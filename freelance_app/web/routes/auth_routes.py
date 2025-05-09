from flask import Blueprint, request, render_template, redirect, url_for, session
from app.use_cases.user_use_cases import RegisterUser
from infrastructure.repositories.sqlalchemy_repo import SQLAlchemyUserRepo
from infrastructure.services.auth_service_impl import SimpleAuthService
from app.use_cases.login_user import LoginUser
import traceback

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        use_case = RegisterUser(SQLAlchemyUserRepo(), SimpleAuthService())
        try:
            user = use_case.execute({
                "email": data["email"],
                "password": data["password"],
                "role": data["role"],
                "name": data["name"]
            })
            return f"User {user.email} registered successfully."
        except Exception as e:
            traceback.print_exc()
            return f"Error: {str(e)}"
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        use_case = LoginUser(SQLAlchemyUserRepo(), SimpleAuthService())
        try:
            user = use_case.execute(data["email"], data["password"])
            session["user_email"] = user.email
            session["user_role"] = user.role
            session["user_name"] = user.name

            if user.role == "client":
                return redirect(url_for("main.client_dashboard"))
            else:
                return redirect(url_for("main.freelancer_dashboard"))
        except Exception as e:
            return f"Login failed: {str(e)}"
    return render_template("login.html")


@auth_bp.route("/client/dashboard")
def client_dashboard():
    if 'user_id' not in session or session['role'] != 'client':
        return redirect(url_for('auth.login'))
    return render_template("client_dashboard.html")

@auth_bp.route("/freelancer/dashboard")
def freelancer_dashboard():
    if 'user_id' not in session or session['role'] != 'freelancer':
        return redirect(url_for('auth.login'))
    return render_template("freelancer_dashboard.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route("/client/jobs")
def client_jobs():
    if 'user_id' not in session or session['role'] != 'client':
        return redirect(url_for('auth.login'))
    jobs = [
        {"title": "Web Development", "description": "Build a website for a client"},
        {"title": "Mobile App", "description": "Develop an iOS app"}
    ]
    return render_template("client_dashboard.html", jobs=jobs)

@auth_bp.route("/freelancer/jobs")
def freelancer_jobs():
    if 'user_id' not in session or session['role'] != 'freelancer':
        return redirect(url_for('auth.login'))
    # Here you would query available jobs from the database
    jobs = [
        {"title": "Web Development", "description": "Build a website for a client"},
        {"title": "Mobile App", "description": "Develop an iOS app"}
    ]
    return render_template("freelancer_dashboard.html", jobs=jobs)
