from typing import List
from app.domain.models import Offer
from app.domain.interfaces import OfferRepository

class ListFreelancerOffers:
    def __init__(self, offer_repo: OfferRepository):
        self.offer_repo = offer_repo

    def execute(self, freelancer_id: int) -> List[Offer]:
        return self.offer_repo.get_offers_by_freelancer(freelancer_id)
