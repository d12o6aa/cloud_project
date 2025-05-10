from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    id: int | None = None
    name: str = ""
    email: str = ""
    password: str = ""
    role: str = ""

@dataclass
class Job:
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    budget: float = 0.0
    deadline: datetime = datetime.now()
    client_id: int = 0
    status: str = "open"

@dataclass
class Offer:
    id: Optional[int] = None
    job_id: int = 0
    freelancer_id: int = 0
    amount: float = 0.0
    message: str = ""
    status: str = "pending"
