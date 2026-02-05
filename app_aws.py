#PROPERRR


from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import boto3
import uuid
from boto3.dynamodb.conditions import Attr

app = Flask(__name__)
app.secret_key = "greenfield_university_secret"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ==========================================
# AWS CONFIGURATION (Greenfield Infrastructure)
# ==========================================
REGION = "us-east-1" 
SNS_TOPIC_ARN = "PASTE_YOUR_SNS_TOPIC_ARN_HERE"

# AWS Service Clients
dynamodb = boto3.resource("dynamodb", region_name=REGION)
sns = boto3.client("sns", region_name=REGION)

# Tables
STUDENTS_TABLE = dynamodb.Table("Students")
BOOKS_TABLE = dynamodb.Table("Books")
REQUESTS_TABLE = dynamodb.Table("Requests")

class User(UserMixin):
    def __init__(self, email, role):
        self.id = email
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    # Predefined Staff Account
    if user_id == "staff@library.com":
        return User(user_id, "staff")
    try:
        student = STUDENTS_TABLE.get_item(Key={"email": user_id})
        if "Item" in student:
            return User(user_id, "student")
    except:
        pass
    return None

# ==========================================
# ROUTES
# ==========================================

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
        # Store in DynamoDB instead of local dictionary
        STUDENTS_TABLE.put_item(Item={
            "email": data["email"],
            "password": data["password"],
            "name": data["name"],
            "roll_no": data["roll_no"],
            "semester": data["semester"],
            "year": data["year"]
        })
        flash("Registration Successful!", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email, password, role = request.form["email"], request.form["password"], request.form["role"]
        
        # Staff Login
        if role == "staff" and email == "staff@library.com" and password == "staff123":
            login_user(User(email, "staff"))
            return redirect(url_for("staff_dashboard"))
        
        # Student Login via DynamoDB
        res = STUDENTS_TABLE.get_item(Key={"email": email})
        if "Item" in res and res["Item"]["password"] == password:
            login_user(User(email, "student"))
            return redirect(url_for("dashboard"))
            
        flash("Invalid Credentials", "danger")
    return render_template("login.html")

# SCENARIO 1 & 3: Student Access & S3 Resources
@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "student": return redirect(url_for("home"))
    
    # 1. Fetch Books from DynamoDB and format for template
    books_data = BOOKS_TABLE.scan()["Items"]
    # Reconstruct the dictionary format: { "B101": {title: ..., s3_url: ...} }
    books_dict = {b["book_id"]: b for b in books_data}
    
    # 2. Fetch specific requests for current student
    my_requests = REQUESTS_TABLE.scan(
        FilterExpression=Attr("student_email").eq(current_user.id)
    )["Items"]
    
    return render_template("dashboard.html", books=books_dict, my_requests=my_requests)

# SCENARIO 2: SNS Notification Trigger
@app.route("/request/<book_id>")
@login_required
def request_book(book_id):
    # Fetch book details from DynamoDB
    book_res = BOOKS_TABLE.get_item(Key={"book_id": book_id})
    book = book_res["Item"]
    
    req_id = str(uuid.uuid4())
    
    # Create Request in DynamoDB
    REQUESTS_TABLE.put_item(Item={
        "id": req_id,
        "book_id": book_id,
        "student_email": current_user.id,
        "book": book["title"],
        "status": "Pending"
    })

    # TRIGGER REAL AWS SNS
    try:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"New Request: Student {current_user.id} requested '{book['title']}'.",
            Subject="Greenfield Library - New Request"
        )
    except Exception as e:
        print(f"SNS Error: {e}")

    flash("Request sent! Staff notified via SNS.", "success")
    return redirect(url_for("dashboard"))

@app.route("/staff")
@login_required
def staff_dashboard():
    if current_user.role != "staff": return redirect(url_for("home"))
    
    # Fetch all requests for staff view
    requests = REQUESTS_TABLE.scan()["Items"]
    return render_template("staff_dashboard.html", requests=requests)

# SCENARIO 3: Digital S3 Access Update (Matches local logic)
@app.route("/staff/update_status/<request_id>/<new_status>")
@login_required
def update_status(request_id, new_status):
    if current_user.role != "staff": return redirect(url_for("home"))
    
    # 1. Get request details
    req_res = REQUESTS_TABLE.get_item(Key={"id": request_id})
    req = req_res["Item"]
    
    # 2. Update Request Status in DynamoDB
    REQUESTS_TABLE.update_item(
        Key={"id": request_id},
        UpdateExpression="SET #st = :val",
        ExpressionAttributeNames={"#st": "status"},
        ExpressionAttributeValues={":val": new_status}
    )

    # 3. Flip availability in Books Table if marked Available
    if new_status == "Available":
        BOOKS_TABLE.update_item(
            Key={"book_id": req["book_id"]},
            UpdateExpression="SET available = :val",
            ExpressionAttributeValues={":val": True}
        )
        
        # Notify student via SNS
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"Your book '{req['book']}' is now Available for download.",
            Subject="Greenfield Library - Request Approved"
        )

    return redirect(url_for("staff_dashboard"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) # Standard for EC2 deployment