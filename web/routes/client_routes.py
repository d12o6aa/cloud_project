from flask import Blueprint, render_template, session, redirect, url_for, request, flash
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
    status = request.args.get("status")  # open, closed, etc.

    job_repo = SQLAlchemyJobRepo()
    if status:
        jobs = job_repo.get_by_client_and_status(client_id, status)
    else:
        jobs = ListClientJobs(job_repo).execute(client_id)
    
    return render_template("client_jobs.html", jobs=jobs, status_filter=status)



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

@client_bp.route("/offers/<int:offer_id>/accept", methods=["POST"])
def accept_offer(offer_id):
    repo = SQLAlchemyOfferRepo()
    repo.update_status(offer_id, "accepted")
    
    job_id = repo.get_offer_by_id(offer_id).job_id
    job_repo = SQLAlchemyJobRepo()
    job_repo.update_status(job_id, "closed")
    
    flash("Offer accepted and job closed.")
    return redirect(url_for("client.client_jobs"))


@client_bp.route("/offers/<int:offer_id>/reject", methods=["POST"])
def reject_offer(offer_id):
    repo = SQLAlchemyOfferRepo()
    repo.update_status(offer_id, "rejected")
    flash("Offer rejected.")
    return redirect(url_for("client.client_jobs"))

@client_bp.route("/offers/action", methods=["POST"], endpoint="client_offer_action")
def client_offer_action():
    if "user_id" not in session or session.get("user_role") != "client":
        return redirect(url_for("auth.auth_login"))

    offer_id = request.form.get("offer_id")
    action = request.form.get("action")

    repo = SQLAlchemyOfferRepo()
    if action == "accept":
        repo.update_offer_status(offer_id, "accepted")
        offer = repo.get_by_id(offer_id)
        job_repo = SQLAlchemyJobRepo()
        job_repo.update_status(offer.job_id, "closed")
    elif action == "reject":
        repo.update_offer_status(offer_id, "rejected")

    return redirect(url_for("client.client_offers"))