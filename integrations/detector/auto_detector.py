# Python
import json
import hashlib

# Managers
from modules.telephone.managers.auto_detection import AutoDetectionRecords

# Libs
import requests
from integrations.detector.constants import PROMPT
from integrations.detector.types import AutoDetect
from core.settings import OPENIA_API_KEY, OPENIA_API_ENDPOINT


def make_client_request(number: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENIA_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": number},
        ],
    }

    resp = requests.post(
        OPENIA_API_ENDPOINT,
        headers=headers,
        json=payload,
    )
    return resp.json()["choices"][0]["message"]["content"]


def auto_detect_phone_info(number: str) -> AutoDetect:

    number_hash = hashlib.sha256(number.encode()).hexdigest()
    existing_record = AutoDetectionRecords.objects.get_record_from_hash(number_hash)

    if not existing_record:
        response = make_client_request(number)

        # Clean the json before formatter the JSON
        data = response.replace("json", "").replace("```", "").replace("\n", "")
        loaded_data = json.loads(data)

        indicative = loaded_data["indicative"]
        country = loaded_data["country"]
        number = loaded_data["number"]

        AutoDetectionRecords.objects.create(
            number=number,
            hash=number_hash,
            code_region=indicative,
            country_code=country,
        )
    else:
        indicative = existing_record.code_region
        country = existing_record.country_code
        number = existing_record.number

    return AutoDetect(
        indicative=indicative,
        country=country,
        number=number,
    )
