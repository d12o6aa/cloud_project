from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from infrastructure.db.database import Base

class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    budget = Column(Float)
    deadline = Column(DateTime)
    client_id = Column(Integer)
    status = Column(String, default="open")
