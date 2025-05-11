from app.domain.interfaces import JobRepository

class ListOpenJobs:
    def __init__(self, job_repo: JobRepository):
        self.job_repo = job_repo

    def execute(self):
        return self.job_repo.list_open_jobs()
