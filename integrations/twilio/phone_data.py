# Python
import hashlib
from datetime import datetime

# Models
from modules.telephone.managers.phone_metadata import PhoneMetadataRecords

# Libs
import requests
import humanize

from core.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN


def make_client_request(number: str) -> dict:
    url = f"https://lookups.twilio.com/v2/PhoneNumbers/{number}"
    params = {"Fields": "sms_pumping_risk,line_type_intelligence"}
    resp = requests.get(
        url,
        params=params,
        auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
    )

    resp.raise_for_status()
    data = resp.json()
    return {
        "line_type_intelligence": data["line_type_intelligence"],
        "sms_pumping_risk": data["sms_pumping_risk"],
    }


def get_phone_metadata(number: str) -> dict:

    number_hash = hashlib.sha256(number.encode()).hexdigest()
    existing_record = PhoneMetadataRecords.objects.get_record_from_hash(number_hash)

    carrier_phone_info = None
    security_phone_info = None

    if not existing_record:
        record = make_client_request(number)
        line_type_intelligence = record["line_type_intelligence"]
        sms_pumping_risk = record["sms_pumping_risk"]

        PhoneMetadataRecords.objects.create(
            hash=number_hash,
            carrier=line_type_intelligence,
            security=sms_pumping_risk,
        )
    else:
        line_type_intelligence = existing_record.carrier
        sms_pumping_risk = existing_record.security

    if line_type_intelligence:
        carrier_phone_info = {
            "type": line_type_intelligence.get("type"),
            "carrier": {
                "name": line_type_intelligence.get("carrier_name"),
                "mcc": line_type_intelligence.get("mobile_country_code"),
                "mnc": line_type_intelligence.get("mobile_network_code"),
            },
        }

    if sms_pumping_risk:
        blocked_date = sms_pumping_risk.get("number_blocked_date")
        security_phone_info = {
            "spam_score": sms_pumping_risk.get("sms_pumping_risk_score"),
            "risk_category": sms_pumping_risk.get("carrier_risk_category"),
            "number_blocked": sms_pumping_risk.get("number_blocked"),
            "blocked_in_last_3_months": bool(
                sms_pumping_risk.get("number_blocked_last_3_months"),
            ),
            "last_blocked_at": None,
        }

        if blocked_date:
            security_phone_info["last_blocked_at"] = humanize.naturaldate(
                datetime.fromisoformat(blocked_date),
            )
        else:
            security_phone_info["last_blocked_at"] = "--"

    return {
        "carrier": carrier_phone_info,
        "security": security_phone_info,
    }
