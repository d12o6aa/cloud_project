from flask import Blueprint,request, render_template, session, redirect, url_for
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
    offers = ListFreelancerOffers(SQLAlchemyOfferRepo()).execute(freelancer_id)
    return render_template("freelancer_dashboard.html", offers=offers)

# @freelance_bp.route("/offers/create", methods=["GET", "POST"], endpoint="create_offer")
# def create_offer():
#     if "user_id" not in session or session.get("user_role") != "freelancer":
#         return redirect(url_for("auth.auth_login"))

#     if request.method == "POST":
#         job_id = request.form["job_id"]
#         amount = float(request.form["amount"])
#         message = request.form["message"]
#         freelancer_id = session["user_id"]

#         offer = Offer(
#             job_id=int(job_id),
#             freelancer_id=freelancer_id,
#             amount=amount,
#             message=message,
#             status="pending"
#         )
#         SQLAlchemyOfferRepo().create(offer)
#         return redirect(url_for("freelancer.freelancer_offers"))

#     jobs = SQLAlchemyJobRepo().list_open_jobs()
#     return render_template("create_offer.html", jobs=jobs)

@freelance_bp.route("/offers", endpoint="freelancer_offers")
def freelancer_offers():
    if "user_id" not in session or session.get("user_role") != "freelancer":
        return redirect(url_for("auth.auth_login"))

    freelancer_id = session["user_id"]
    offers = ListFreelancerOffers(SQLAlchemyOfferRepo()).execute(freelancer_id)
    jobs = SQLAlchemyJobRepo().list_open_jobs()  # عرض الوظائف المتاحة
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
