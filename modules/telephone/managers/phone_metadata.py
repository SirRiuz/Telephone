# Python
from typing import Optional

# Libs
from sqlalchemy.exc import DatabaseError
from modules.telephone.models.number_metadata import PhoneMetadataRecord


class PhoneMetadataRecordManager:

    def get_record_from_hash(self, hash) -> Optional[PhoneMetadataRecord]:
        queryset = (
            PhoneMetadataRecord.query()
            .filter(
                (PhoneMetadataRecord.is_active == True),
                (PhoneMetadataRecord.hash == hash),
            )
            .first()
        )
        return queryset

    def create(
        self,
        hash: str,
        carrier: dict,
        security: dict,
    ) -> PhoneMetadataRecord:
        try:
            session = PhoneMetadataRecord.query().session
            record = PhoneMetadataRecord(
                hash=hash,
                carrier=carrier,
                security=security,
            )
            session.add(record)
            session.commit()
            return record
        except DatabaseError as e:
            session.rollback()
            session.close()
            raise e


class PhoneMetadataRecords:
    objects = PhoneMetadataRecordManager()
