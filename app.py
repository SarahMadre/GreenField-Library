# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# import uuid

# app = Flask(__name__)
# app.secret_key = "instant_library_secret"

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"

# # =========================
# # DATABASE (DICTIONARIES)
# # =========================

# # Students
# students = {}

# # Staff (predefined)
# staff_users = {
#     "staff@library.com": "staff123"
# }

# # Books Catalog
# books = {
#     "B101": {"title": "Engineering Mathematics", "subject": "Mathematics", "available": False},
#     "B102": {"title": "Discrete Mathematics", "subject": "Mathematics", "available": True},
#     "B201": {"title": "English Grammar & Composition", "subject": "English", "available": False},
#     "B202": {"title": "Professional Communication", "subject": "English", "available": True}
# }

# # Requests
# requests_db = []

# # =========================
# # USER MODEL
# # =========================
# class User(UserMixin):
#     def __init__(self, email, role):
#         self.id = email
#         self.role = role

# @login_manager.user_loader
# def load_user(user_id):
#     if user_id in students:
#         return User(user_id, "student")
#     if user_id in staff_users:
#         return User(user_id, "staff")
#     return None

# # =========================
# # ROUTES
# # =========================

# @app.route("/")
# def home():
#     return render_template("home.html")

# @app.route("/about")
# def about():
#     return render_template("about.html")

# @app.route("/contact")
# def contact():
#     return render_template("contact.html")

# # ---------- REGISTER ----------
# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         email = request.form["email"]
#         password = request.form["password"]
#         name = request.form["name"]
#         roll_no = request.form["roll_no"]
#         semester = request.form["semester"]
#         year = request.form["year"]

#         if email in students:
#             flash("Student already exists!", "danger")
#             return redirect(url_for("register"))

#         students[email] = {
#             "password": password,
#             "name": name,
#             "roll_no": roll_no,
#             "semester": semester,
#             "year": year
#         }

#         flash("Registration successful! Please login.", "success")
#         return redirect(url_for("login"))

#     return render_template("register.html")

# # ---------- LOGIN ----------
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form["email"]
#         password = request.form["password"]
#         role = request.form["role"]

#         if role == "student" and email in students and students[email]["password"] == password:
#             login_user(User(email, "student"))
#             return redirect(url_for("dashboard"))

#         if role == "staff" and email in staff_users and staff_users[email] == password:
#             login_user(User(email, "staff"))
#             return redirect(url_for("staff_dashboard"))

#         flash("Invalid credentials", "danger")

#     return render_template("login.html")

# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     flash("Logged out successfully", "info")
#     return redirect(url_for("home"))

# # ---------- STUDENT DASHBOARD ----------
# @app.route("/dashboard")
# @login_required
# def dashboard():
#     if current_user.role != "student":
#         return redirect(url_for("home"))

#     my_requests = [r for r in requests_db if r["student_email"] == current_user.id]
#     return render_template("dashboard.html", books=books, my_requests=my_requests)

# # ---------- REQUEST BOOK ----------
# @app.route("/request/<book_id>")
# @login_required
# def request_book(book_id):
#     if current_user.role != "student":
#         return redirect(url_for("home"))

#     request_entry = {
#         "id": str(uuid.uuid4()),
#         "student_email": current_user.id,
#         "student_name": students[current_user.id]["name"],
#         "roll_no": students[current_user.id]["roll_no"],
#         "semester": students[current_user.id]["semester"],
#         "year": students[current_user.id]["year"],
#         "book_id": book_id,
#         "book": books[book_id]["title"],
#         "subject": books[book_id]["subject"],
#         "description": f"Request for {books[book_id]['title']}",
#         "status": "Pending"
#     }

#     requests_db.append(request_entry)

#     flash("Request submitted successfully!", "success")

#     print("\n📧 EMAIL TO STAFF (SIMULATED)")
#     print("New request for:", books[book_id]["title"])
#     print("From student:", current_user.id)

#     return redirect(url_for("dashboard"))

# # ---------- STAFF DASHBOARD ----------
# @app.route("/staff")
# @login_required
# def staff_dashboard():
#     if current_user.role != "staff":
#         return redirect(url_for("home"))
#     return render_template("staff_dashboard.html", requests=requests_db)

# # ---------- STAFF UPDATE STATUS ----------
# @app.route("/staff/update_status/<request_id>/<new_status>")
# @login_required
# def update_status(request_id, new_status):
#     if current_user.role != "staff":
#         return redirect(url_for("home"))

#     for r in requests_db:
#         if r["id"] == request_id:
#             r["status"] = new_status
#             if new_status == "Available":
#                 books[r["book_id"]]["available"] = True

#             # Simulate SNS notification
#             print("\n📧 EMAIL TO STUDENT (SIMULATED)")
#             print("Book:", r["book"])
#             print("Status updated to:", new_status)
#             print("Student:", r["student_email"])
#             break

#     return redirect(url_for("staff_dashboard"))

# # =========================
# # RUN APP
# # =========================
# if __name__ == "__main__":
#     app.run(debug=True)




from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import uuid

app = Flask(__name__)
app.secret_key = "instant_library_secret"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# =========================
# DATABASE (SIMULATED)
# =========================

students = {}
staff_users = {"staff@library.com": "staff123"}

# Scenario 3: Books include S3 URLs. 
# REPLACE the URLs below with your actual S3 Object URLs.
books = {
    "B101": {
        "title": "Engineering Mathematics", 
        "subject": "Mathematics", 
        "available": False,
        "s3_url": "https://greenfield-library-storage.s3.amazonaws.com/math_textbook.pdf"
    },
    "B102": {
        "title": "Discrete Mathematics", 
        "subject": "Mathematics", 
        "available": True,
        "s3_url": "https://greenfield-library-storage.s3.amazonaws.com/discrete_math.pdf"
    },
    "B201": {
        "title": "English Grammar & Composition", 
        "subject": "English", 
        "available": False,
        "s3_url": "https://greenfield-library-storage.s3.amazonaws.com/english_grammar.pdf"
    }
}

requests_db = []

class User(UserMixin):
    def __init__(self, email, role):
        self.id = email
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    if user_id in students: return User(user_id, "student")
    if user_id in staff_users: return User(user_id, "staff")
    return None

# =========================
# ROUTES
# =========================

@app.route("/")
def home(): return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        students[email] = {
            "password": request.form["password"],
            "name": request.form["name"],
            "roll_no": request.form["roll_no"],
            "semester": request.form["semester"],
            "year": request.form["year"]
        }
        flash("Registration successful!", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email, pwd, role = request.form["email"], request.form["password"], request.form["role"]
        if role == "student" and email in students and students[email]["password"] == pwd:
            login_user(User(email, "student"))
            return redirect(url_for("dashboard"))
        if role == "staff" and email in staff_users and staff_users[email] == pwd:
            login_user(User(email, "staff"))
            return redirect(url_for("staff_dashboard"))
        flash("Invalid credentials", "danger")
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "student": return redirect(url_for("home"))
    my_requests = [r for r in requests_db if r["student_email"] == current_user.id]
    return render_template("dashboard.html", books=books, my_requests=my_requests)

@app.route("/request/<book_id>")
@login_required
def request_book(book_id):
    req_id = str(uuid.uuid4())
    request_entry = {
        "id": req_id,
        "student_email": current_user.id,
        "book_id": book_id,
        "book": books[book_id]["title"],
        "status": "Pending"
    }
    requests_db.append(request_entry)
    
    # SIMULATED SNS
    print(f"\n--- AWS SNS: Staff notified that {current_user.id} requested {books[book_id]['title']} ---\n")
    
    flash("Request submitted! Staff notified via SNS simulation.", "success")
    return redirect(url_for("dashboard"))

@app.route("/staff")
@login_required
def staff_dashboard():
    if current_user.role != "staff": return redirect(url_for("home"))
    return render_template("staff_dashboard.html", requests=requests_db)

@app.route("/staff/update_status/<request_id>/<new_status>")
@login_required
def update_status(request_id, new_status):
    for r in requests_db:
        if r["id"] == request_id:
            r["status"] = new_status
            if new_status == "Available":
                books[r["book_id"]]["available"] = True
            print(f"\n--- AWS SNS: Student {r['student_email']} notified that book is {new_status} ---\n")
            break
    return redirect(url_for("staff_dashboard"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)