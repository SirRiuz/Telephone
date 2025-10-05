# Python
from typing import Optional

# Libs
from sqlalchemy.exc import DatabaseError
from modules.telephone.models.auto_detection import AutoDetectionRecord


class AutoDetectionRecordManager:

    def get_record_from_hash(self, hash) -> Optional[AutoDetectionRecord]:
        """"""
        queryset = (
            AutoDetectionRecord.query()
            .filter(
                (AutoDetectionRecord.is_active == True),
                (AutoDetectionRecord.hash == hash),
            )
            .first()
        )
        return queryset

    def create(
        self,
        hash: str,
        number: int,
        code_region: str,
        country_code: str,
    ) -> AutoDetectionRecord:
        """ """
        try:
            session = AutoDetectionRecord.query().session
            record = AutoDetectionRecord(
                hash=hash,
                number=number,
                code_region=code_region,
                country_code=country_code,
            )
            session.add(record)
            session.commit()
            return record
        except DatabaseError as e:
            session.rollback()
            session.close()
            raise e


class AutoDetectionRecords:
    objects = AutoDetectionRecordManager()
