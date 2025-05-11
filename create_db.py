from infrastructure.db.database import engine, Base
from infrastructure.models.user_model import UserModel
from infrastructure.models.job_model import JobModel
from infrastructure.models.offer_model import OfferModel

Base.metadata.create_all(bind=engine)
