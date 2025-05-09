from infrastructure.db.database import SessionLocal
from infrastructure.models.user_model import UserModel
from app.domain.models import User
from app.domain.interfaces import UserRepository
from app.domain.models import Job
from app.domain.interfaces import JobRepository
from infrastructure.models.job_model import JobModel
from app.domain.models import Offer
from app.domain.interfaces import OfferRepository
from infrastructure.models.offer_model import OfferModel

class SQLAlchemyUserRepo(UserRepository):
    def get_by_email(self, email: str) -> User | None:
        db = SessionLocal()
        user_model = db.query(UserModel).filter_by(email=email).first()
        db.close()
        if user_model:
            return User(
                name=user_model.name,
                email=user_model.email,
                password=user_model.password,
                role=user_model.role
            )
        return None

    def save(self, user: User) -> User:
        db = SessionLocal()
        db_user = UserModel(
            name=user.name,
            email=user.email,
            password=user.password,
            role=user.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        db.close()
        return user
    
    def create(self, user: User) -> User:
        db = SessionLocal()
        existing_user = db.query(UserModel).filter_by(email=user.email).first()
        if existing_user:
            db.close()
            raise ValueError(f"User with email {user.email} already exists.")
        
        db_user = UserModel(
            name=user.name,
            email=user.email,
            password=user.password,
            role=user.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        db.close()
        return user


class SQLAlchemyJobRepo(JobRepository):
    def list_open_jobs(self) -> list[Job]:
        db = SessionLocal()
        jobs = db.query(JobModel).filter(JobModel.status == "open").all()
        db.close()
        return [Job(
            id=job.id,
            title=job.title,
            description=job.description,
            budget=job.budget,
            deadline=job.deadline,
            client_id=job.client_id,
            status=job.status
        ) for job in jobs]

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

    def list_by_job(self, job_id: int) -> list[Offer]:
        db = SessionLocal()
        offers = db.query(OfferModel).filter_by(job_id=job_id).all()
        db.close()
        return [Offer(
            id=offer.id,
            job_id=offer.job_id,
            freelancer_id=offer.freelancer_id,
            amount=offer.amount,
            message=offer.message,
            status=offer.status
        ) for offer in offers]