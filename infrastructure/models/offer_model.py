from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db.database import Base

class OfferModel(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    freelancer_id = Column(Integer)
    amount = Column(Float)
    message = Column(String)
    status = Column(String, default="pending")
    job = relationship("JobModel", backref="offers")