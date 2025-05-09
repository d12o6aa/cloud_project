from app.domain.models import Job
from infrastructure.models.job_model import JobModel
from infrastructure.db.database import SessionLocal
from app.domain.interfaces import JobRepository

class SQLAlchemyJobRepo(JobRepository):
    def list_open_jobs(self):
        db = SessionLocal()
        jobs = db.query(JobModel).filter_by(status="open").all()
        db.close()
        return [Job(**job.__dict__) for job in jobs]

    def create(self, job: Job) -> Job:
        db = SessionLocal()
        db_job = JobModel(
            title=job.title,
            description=job.description,
            budget=job.budget,
            deadline=job.deadline,
            client_id=job.client_id,
            status=job.status
        )
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        db.close()
        job.id = db_job.id
        return job
