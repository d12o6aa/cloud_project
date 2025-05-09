from app.domain.models import Job
from app.domain.interfaces import JobRepository

class CreateJob:
    def __init__(self, job_repo: JobRepository):
        self.job_repo = job_repo

    def execute(self, job_data: dict) -> Job:
        job = Job(
            title=job_data['title'],
            description=job_data['description'],
            budget=job_data['budget'],
            deadline=job_data['deadline'],
            client_id=job_data['client_id']
        )
        return self.job_repo.create(job)

class ListOpenJobs:
    def __init__(self, job_repo: JobRepository):
        self.job_repo = job_repo

    def execute(self) -> list[Job]:
        return self.job_repo.list_open_jobs()
