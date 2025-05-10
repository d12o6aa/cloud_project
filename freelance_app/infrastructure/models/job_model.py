from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from infrastructure.db.database import Base

class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    budget = Column(Float, nullable=False)
    deadline = Column(Date, nullable=False)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="open")