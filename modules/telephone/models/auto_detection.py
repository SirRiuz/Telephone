# Models
from sqlalchemy import Column, String
from core.db.models import Model


class AutoDetectionRecord(Model):
    __tablename__ = "auto_detection_record"
    hash = Column(String(64), nullable=False, unique=True)

    number = Column(String(64), nullable=False)
    code_region = Column(String(64), nullable=False)
    country_code = Column(String(64), nullable=False)
