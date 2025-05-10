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
from typing import List

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

    def find_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
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
        return User(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            password=db_user.password,
            role=db_user.role
        )

    
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
        return User(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            password=db_user.password,
            role=db_user.role
        )


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

    def list_jobs_by_client(self, client_id: int) -> List[Job]:
        db = SessionLocal()
        jobs = db.query(JobModel).filter_by(client_id=client_id).all()
        db.close()
        return [
            Job(
                id=job.id,
                title=job.title,
                description=job.description,
                budget=job.budget,
                deadline=job.deadline,
                client_id=job.client_id,
                status=job.status
            )
            for job in jobs
        ]
    def list_jobs_by_client_and_status(self, client_id: int, status: str) -> List[Job]:
        db = SessionLocal()
        jobs = db.query(JobModel).filter_by(client_id=client_id, status=status).all()
        db.close()
        return [
            Job(
                id=job.id,
                title=job.title,
                description=job.description,
                budget=job.budget,
                deadline=job.deadline,
                client_id=job.client_id,
                status=job.status
            )
            for job in jobs
        ]
        
    def update_status(self, job_id: int, status: str):
        db = SessionLocal()
        job = db.query(JobModel).filter_by(id=job_id).first()
        if job:
            job.status = status
            db.commit()
        db.close()


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

    def list_by_freelancer(self, freelancer_id: int) -> List[Offer]:
        db = SessionLocal()
        offers = (
            db.query(OfferModel)
            .filter_by(freelancer_id=freelancer_id)
            .join(JobModel)
            .all()
        )
        result = []
        for offer in offers:
            result.append(Offer(
                id=offer.id,
                job_id=offer.job_id,
                job_title=offer.job.title,
                amount=offer.amount,
                message=offer.message,
                freelancer_id=offer.freelancer_id,
                status=offer.status
            ))
        db.close()
        return result
 
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
        
    def list_offers_by_client_jobs(self, client_id: int) -> List[Offer]:
        db = SessionLocal()
        offers = (
            db.query(OfferModel)
            .join(JobModel, OfferModel.job_id == JobModel.id)
            .filter(JobModel.client_id == client_id)
            .all()
        )
        db.close()
        return [
            Offer(
                id=o.id,
                job_id=o.job_id,
                freelancer_id=o.freelancer_id,
                amount=o.amount,
                message=o.message,
                status=o.status
            )
            for o in offers
        ]
    def get_by_id(self, offer_id: int) -> Offer:
        db = SessionLocal()
        offer = db.query(OfferModel).filter_by(id=offer_id).first()
        result = Offer(
            id=offer.id,
            job_id=offer.job_id,
            freelancer_id=offer.freelancer_id,
            amount=offer.amount,
            message=offer.message,
            status=offer.status
        )
        db.close()
        return result
    def update_offer_status(self, offer_id: int, status: str):
        db = SessionLocal()
        offer = db.query(OfferModel).filter_by(id=offer_id).first()
        if offer:
            offer.status = status
            db.commit()
        db.close()

    def get_by_freelancer_id(self, freelancer_id):
        db = SessionLocal()
        offers = db.query(OfferModel).filter_by(freelancer_id=freelancer_id).all()
        db.close()
        return offers
    
    def get_offers_by_freelancer(self, freelancer_id):
        db = SessionLocal()
        offer_models = db.query(OfferModel).filter_by(freelancer_id=freelancer_id).all()
        db.close()
        return [
            Offer(
                id=o.id,
                job_id=o.job_id,
                freelancer_id=o.freelancer_id,
                amount=o.amount,
                message=o.message,
                status=o.status
            )
            for o in offer_models
        ]
        
    def update_status(self, offer_id: int, status: str):
        db = SessionLocal()
        offer = db.query(OfferModel).filter_by(id=offer_id).first()
        if offer:
            offer.status = status
            db.commit()
        db.close()


