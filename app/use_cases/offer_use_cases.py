from app.domain.models import Offer
from app.domain.interfaces import OfferRepository

class CreateOffer:
    def __init__(self, offer_repo: OfferRepository):
        self.offer_repo = offer_repo

    def execute(self, offer_data: dict) -> Offer:
        offer = Offer(
            job_id=offer_data['job_id'],
            freelancer_id=offer_data['freelancer_id'],
            amount=offer_data['amount'],
            message=offer_data['message']
        )
        return self.offer_repo.create(offer)

class ListOffersForJob:
    def __init__(self, offer_repo: OfferRepository):
        self.offer_repo = offer_repo

    def execute(self, job_id: int) -> list[Offer]:
        return self.offer_repo.list_by_job(job_id)
