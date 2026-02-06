from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import boto3
import uuid
from boto3.dynamodb.conditions import Attr
import os

app = Flask(__name__)
app.secret_key = "greenfield_university_secret"

# --------------------------------------------------
# LOGIN CONFIG
# --------------------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# --------------------------------------------------
# AWS CONFIG (WORKS FOR BOTH MOTO + REAL AWS)
# --------------------------------------------------
REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:376129887113:LibraryRequests:633b8224-013f-4087-bf5e-7627391e14ba"


dynamodb = boto3.resource("dynamodb", region_name=REGION)
sns = boto3.client("sns", region_name=REGION)

STUDENTS_TABLE = dynamodb.Table("Students")
BOOKS_TABLE = dynamodb.Table("Books")
REQUESTS_TABLE = dynamodb.Table("Requests")

# --------------------------------------------------
# USER MODEL
# --------------------------------------------------
class User(UserMixin):
    def __init__(self, email, role):
        self.id = email
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    if user_id == "staff@library.com":
        return User(user_id, "staff")

    try:
        res = STUDENTS_TABLE.get_item(Key={"email": user_id})
        if "Item" in res:
            return User(user_id, "student")
    except:
        pass

    return None

# --------------------------------------------------
# ROUTES
# --------------------------------------------------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        STUDENTS_TABLE.put_item(Item={
            "email": data["email"],
            "password": data["password"],
            "name": data["name"],
            "roll_no": data["roll_no"],
            "semester": data["semester"],
            "year": data["year"]
        })
        flash("Registration successful!", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        if role == "staff" and email == "staff@library.com" and password == "staff123":
            login_user(User(email, "staff"))
            return redirect(url_for("staff_dashboard"))

        res = STUDENTS_TABLE.get_item(Key={"email": email})
        if "Item" in res and res["Item"]["password"] == password:
            login_user(User(email, "student"))
            return redirect(url_for("dashboard"))

        flash("Invalid credentials", "danger")

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "student":
        return redirect(url_for("home"))

    books = BOOKS_TABLE.scan()["Items"]
    books_dict = {b["book_id"]: b for b in books}

    my_requests = REQUESTS_TABLE.scan(
        FilterExpression=Attr("student_email").eq(current_user.id)
    )["Items"]

    return render_template("dashboard.html", books=books_dict, my_requests=my_requests)

@app.route("/request/<book_id>")
@login_required
def request_book(book_id):
    book = BOOKS_TABLE.get_item(Key={"book_id": book_id})["Item"]

    req_id = str(uuid.uuid4())
    REQUESTS_TABLE.put_item(Item={
        "id": req_id,
        "book_id": book_id,
        "student_email": current_user.id,
        "book": book["title"],
        "status": "Pending"
    })

    if SNS_TOPIC_ARN:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"Student {current_user.id} requested '{book['title']}'",
            Subject="Library Book Request"
        )

    flash("Request sent! Staff notified.", "success")
    return redirect(url_for("dashboard"))

@app.route("/staff")
@login_required
def staff_dashboard():
    if current_user.role != "staff":
        return redirect(url_for("home"))

    requests = REQUESTS_TABLE.scan()["Items"]
    return render_template("staff_dashboard.html", requests=requests)

@app.route("/staff/update_status/<request_id>/<new_status>")
@login_required
def update_status(request_id, new_status):
    if current_user.role != "staff":
        return redirect(url_for("home"))

    req = REQUESTS_TABLE.get_item(Key={"id": request_id})["Item"]

    REQUESTS_TABLE.update_item(
        Key={"id": request_id},
        UpdateExpression="SET #s = :val",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":val": new_status}
    )

    if new_status == "Available":
        BOOKS_TABLE.update_item(
            Key={"book_id": req["book_id"]},
            UpdateExpression="SET available = :val",
            ExpressionAttributeValues={":val": True}
        )

        if SNS_TOPIC_ARN:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=f"Your book '{req['book']}' is now available",
                Subject="Book Available"
            )

    return redirect(url_for("staff_dashboard"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
