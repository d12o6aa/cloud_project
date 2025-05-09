from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/client/dashboard")
def client_dashboard():
    if session.get("user_role") != "client":
        return redirect(url_for("auth.login"))
    return render_template("client_dashboard.html", name=session.get("user_name", "Client"))

@main_bp.route("/freelancer/dashboard")
def freelancer_dashboard():
    if session.get("user_role") != "freelancer":
        return redirect(url_for("auth.login"))
    return render_template("freelancer_dashboard.html", name=session.get("user_name", "Freelancer"))
