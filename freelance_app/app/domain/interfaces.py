from abc import ABC, abstractmethod
from typing import List
from .models import User, Job, Offer

class UserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass

class JobRepository(ABC):
    @abstractmethod
    def list_open_jobs(self) -> List[Job]:
        pass

    @abstractmethod
    def create(self, job: Job) -> Job:
        pass

class OfferRepository(ABC):
    @abstractmethod
    def create(self, offer: Offer) -> Offer:
        pass
    
    @abstractmethod
    def list_by_job(self, job_id: int) -> List[Offer]:
        pass


class UserRepository:
    def save(self, user: User) -> User:
        raise NotImplementedError

    def get_by_email(self, email: str) -> User:
        raise NotImplementedError

class AuthService(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, plain: str, hashed: str) -> bool:
        pass

    @abstractmethod
    def create_token(self, user_id: int) -> str:
        pass
