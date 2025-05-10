from flask import Blueprint, render_template, session, redirect, url_for, request
from infrastructure.models.job_model import JobModel
from infrastructure.repositories.sqlalchemy_repo import SQLAlchemyJobRepo, SQLAlchemyOfferRepo
from app.use_cases.client_use_cases import ListClientJobs, ListClientOffers
from datetime import datetime

client_bp = Blueprint("client", __name__)




@client_bp.route("/jobs", endpoint="client_jobs")
def client_jobs():
    print("Session:", session)
    if "user_id" not in session or session.get("user_role") != "client":
        return redirect(url_for("auth.auth_login"))
    
    client_id = session["user_id"]
    jobs = ListClientJobs(SQLAlchemyJobRepo()).execute(client_id)
    return render_template("client_jobs.html", jobs=jobs)



@client_bp.route("/offers", endpoint="client_offers")
def client_offers():
    print("Session:", session)
    if "user_id" not in session or session.get("user_role") != "client":
        return redirect(url_for("auth.auth_login"))

    client_id = session["user_id"]
    offers = ListClientOffers(SQLAlchemyOfferRepo()).execute(client_id)
    return render_template("client_offers.html", offers=offers)


@client_bp.route("/create", methods=["GET", "POST"])
def create_job():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        budget = float(request.form["budget"])
        deadline_str = request.form["deadline"]
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()  # 👈 التحويل هنا
        client_id = session.get("user_id") 

        job = JobModel(
            title=title,
            description=description,
            budget=budget,
            deadline=deadline,
            client_id=client_id,
            status="open" 
        )
        db = SQLAlchemyJobRepo()
        db.create(job)
        return redirect(url_for("client.client_dashboard"))

    return render_template("create_job.html")



@client_bp.route("/dashboard", endpoint="client_dashboard")
def client_dashboard():
    if "user_id" not in session or session.get("user_role") != "client":
        return redirect(url_for("auth.auth_login"))

    client_id = session["user_id"]
    jobs = ListClientJobs(SQLAlchemyJobRepo()).execute(client_id)
    return render_template("client_dashboard.html", jobs=jobs)

