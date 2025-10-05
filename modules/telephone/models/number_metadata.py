# Models
from sqlalchemy import Column, String, JSON
from core.db.models import Model


class PhoneMetadataRecord(Model):
    __tablename__ = "phone_metadata_record"
    hash = Column(String(64), nullable=False, unique=True)

    carrier = Column(JSON)
    security = Column(JSON)
