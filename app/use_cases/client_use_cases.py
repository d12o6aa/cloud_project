from typing import List
from app.domain.models import Job, Offer
from app.domain.interfaces import JobRepository, OfferRepository

class ListClientJobs:
    def __init__(self, job_repo: JobRepository):
        self.job_repo = job_repo

    def execute(self, client_id: int) -> List[Job]:
        return self.job_repo.list_jobs_by_client(client_id)

class ListClientOffers:
    def __init__(self, offer_repo: OfferRepository):
        self.offer_repo = offer_repo

    def execute(self, client_id: int) -> List[Offer]:
        return self.offer_repo.list_offers_by_client_jobs(client_id)
