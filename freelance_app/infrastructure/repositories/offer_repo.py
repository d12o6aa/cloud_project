from app.domain.models import Offer
from infrastructure.models.offer_model import OfferModel
from infrastructure.db.database import SessionLocal
from app.domain.interfaces import OfferRepository

class SQLAlchemyOfferRepo(OfferRepository):
    def create(self, offer: Offer) -> Offer:
        db = SessionLocal()
        db_offer = OfferModel(
            job_id=offer.job_id,
            freelancer_id=offer.freelancer_id,
            amount=offer.amount,
            message=offer.message,
            status=offer.status
        )
        db.add(db_offer)
        db.commit()
        db.refresh(db_offer)
        db.close()
        offer.id = db_offer.id
        return offer

    def get_offers_by_freelancer(self, freelancer_id):
        return Offer.query.filter_by(freelancer_id=freelancer_id).all()