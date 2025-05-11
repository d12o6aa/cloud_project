from flask import Blueprint, request, render_template
from app.use_cases.offer_use_cases import CreateOffer
from infrastructure.repositories.sqlalchemy_repo import SQLAlchemyOfferRepo

offer_bp = Blueprint("offer", __name__)

@offer_bp.route("/create", methods=["GET", "POST"])
def create_offer():
    if request.method == "POST":
        data = request.form
        use_case = CreateOffer(SQLAlchemyOfferRepo())
        try:
            offer = use_case.execute({
                "job_id": int(data["job_id"]),
                "freelancer_id": int(data["freelancer_id"]),
                "amount": float(data["amount"]),
                "message": data["message"]
            })
            return f"Offer sent successfully!"
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template("create_offer.html")
