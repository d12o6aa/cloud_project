from flask import Blueprint,request, render_template, session, redirect, url_for, flash
from infrastructure.repositories.sqlalchemy_repo import SQLAlchemyOfferRepo, SQLAlchemyJobRepo
from app.use_cases.list_freelancer_offers import ListFreelancerOffers
from app.use_cases.list_open_jobs import ListOpenJobs

from app.domain.models import Offer
freelance_bp = Blueprint("freelancer", __name__)


@freelance_bp.route("/dashboard", endpoint="freelancer_dashboard")
def freelancer_dashboard():
    if "user_id" not in session or session.get("user_role") != "freelancer":
        return redirect(url_for("auth.auth_login"))

    freelancer_id = session["user_id"]
    jobs = SQLAlchemyJobRepo().list_open_jobs()
    offers = SQLAlchemyOfferRepo().list_by_freelancer(freelancer_id)

    return render_template("freelancer_dashboard.html", jobs=jobs, offers=offers)

@freelance_bp.route("/offers", endpoint="freelancer_offers")
def freelancer_offers():
    if "user_id" not in session or session.get("user_role") != "freelancer":
        return redirect(url_for("auth.auth_login"))

    freelancer_id = session["user_id"]
    offers = ListFreelancerOffers(SQLAlchemyOfferRepo()).execute(freelancer_id)
    jobs = SQLAlchemyJobRepo().list_open_jobs()
    return render_template("freelancer_offers.html", offers=offers, jobs=jobs)

@freelance_bp.route("/offers/create/<job_id>", methods=["GET", "POST"], endpoint="create_offer")
def create_offer(job_id):
    if "user_id" not in session or session.get("user_role") != "freelancer":
        return redirect(url_for("auth.auth_login"))

    freelancer_id = session["user_id"]

    if request.method == "POST":
        amount = request.form["amount"]
        message = request.form["message"]

        offer = Offer(
            job_id=job_id,
            freelancer_id=freelancer_id,
            amount=amount,
            message=message,
            status="pending"
        )
        offer_repo = SQLAlchemyOfferRepo()
        offer_repo.create(offer)

        return redirect(url_for("freelancer.freelancer_offers"))

    return render_template("create_offer.html", job_id=job_id)

@freelance_bp.route("/jobs", endpoint="freelancer_jobs")
def freelancer_jobs():
    if "user_id" not in session or session.get("user_role") != "freelancer":
        return redirect(url_for("auth.auth_login"))

    jobs = ListOpenJobs(SQLAlchemyJobRepo()).execute()
    return render_template("freelancer_jobs.html", jobs=jobs)


@freelance_bp.route("/apply/<int:job_id>", methods=["POST"])
def apply_to_job(job_id):
    if "user_id" not in session or session.get("user_role") != "freelancer":
        return redirect(url_for("auth.auth_login"))

    freelancer_id = session["user_id"]
    amount = request.form.get("amount")
    message = request.form.get("message")

    offer = Offer(
        job_id=job_id,
        freelancer_id=freelancer_id,
        amount=amount,
        message=message,
        status="pending"
    )

    repo = SQLAlchemyOfferRepo()
    repo.create(offer)

    flash("Offer submitted successfully.")
    return redirect(url_for("freelancer.freelancer_jobs"))

@freelance_bp.route("/my_offers", endpoint="my_offers")
def my_offers():
    if "user_id" not in session or session.get("user_role") != "freelancer":
        return redirect(url_for("auth.auth_login"))
    
    freelancer_id = session["user_id"]
    offers = SQLAlchemyOfferRepo().list_by_freelancer(freelancer_id)
    return render_template("freelancer_offers.html", offers=offers)
