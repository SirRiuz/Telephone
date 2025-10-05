# Python
from dataclasses import asdict
from http import HTTPStatus
import logging

# FastApi
import fastapi
from fastapi.responses import JSONResponse

# Schemas
from modules.telephone.schemas.telephone import TelephoneSchema

# Integrations
from integrations.detector.auto_detector import auto_detect_phone_info
from integrations.twilio.phone_data import get_phone_metadata

# Libs
import phonenumbers
from modules.telephone.constants import (
    PHONE_INDICATIVE,
    AUTO_DETECTION,
    MANUAL_DETECTION,
    PHONE_REGEX,
)
from modules.telephone.methods.phone_utils import (
    get_country_info_by_code_region,
    get_basic_phone_number_info,
    get_formats,
)


logging.basicConfig(level=logging.INFO)
router = fastapi.APIRouter(prefix="/v1/telephone")


@router.post(
    "",
    tags=["Telephone"],
    summary="Retrieves information about a phone number.",
    responses={
        200: {
            "description": "Retrieves detailed information about a phone number.",
            "content": {
                "application/json": {
                    "example": {
                        "input": "+55 11 91234-5678",
                        "detection-mode": "by-code",
                        "country": {
                            "name": "Brazil",
                            "flag": "🇧🇷",
                            "code": "BR",
                            "capital": "Brasília",
                            "timezones": "UTC−05:00",
                            "calling_code": "+55",
                        },
                        "number": {"full": "+55 11912345678", "local": "11912345678", "masked": "+55 1119******78"},
                        "formats": {
                            "E.164": "+5511912345678",
                            "RFC3966": "tel:+55-11-91234-5678",
                            "international": "+55 11 91234-5678",
                            "national": "(11) 91234-5678",
                        },
                        "carrier": {"type": "mobile", "carrier": {"name": "Vivo (Telefonica Brasil)", "mcc": "724", "mnc": "06"}},
                        "security": {
                            "spam_score": 2,
                            "risk_category": "low",
                            "number_blocked": False,
                            "blocked_in_last_3_months": False,
                            "last_blocked_at": "--",
                        },
                    }
                }
            },
        },
        400: {
            "description": "In case the information provided is invalid.",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Invalid number",
                        "details": "The number you entered is not valid",
                    },
                }
            },
        },
    },
)
async def telephone(data: TelephoneSchema) -> JSONResponse:

    is_auto_detect = False
    number = data.number

    if not bool(PHONE_REGEX.fullmatch(number)):
        return JSONResponse(
            {
                "error": "Invalid number",
                "details": "The number you entered is not valid",
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )

    if PHONE_INDICATIVE not in number:
        # If the number does not include a country/area code,
        # a small autodetection process is performed
        # to try to deduce which region it belongs to.
        is_auto_detect = True
        try:
            response = auto_detect_phone_info(number)
            full_number = f"{response.indicative}{response.number}"
            parsed = phonenumbers.parse(full_number, None)
        except Exception as e:
            logging.error(e)
            return JSONResponse(
                {
                    "error": "Auto-detection failed",
                    "details": f"Invalid or unrecognized number: {number}",
                },
                status_code=HTTPStatus.BAD_REQUEST,
            )
        country_code = parsed.country_code
        phone_number = str(parsed.national_number)
        code_region = phonenumbers.region_code_for_number(parsed)
    else:
        try:
            parsed = phonenumbers.parse(number, None)
        except Exception as e:
            logging.error(e)
            return JSONResponse(
                {
                    "error": "Parsing error",
                    "details": "The number you entered is not valid",
                },
                status_code=HTTPStatus.BAD_REQUEST,
            )
        country_code = parsed.country_code
        phone_number = str(parsed.national_number)
        code_region = phonenumbers.region_code_for_number(parsed)
    try:
        basic_number_info = asdict(
            get_basic_phone_number_info(
                country_code,
                phone_number,
            )
        )
        number_metadata = get_phone_metadata(f"+{country_code} {phone_number}")
        country_info = asdict(get_country_info_by_code_region(code_region))
        number_formats = get_formats(phone_number, code_region)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            {
                "error": "Something is not right",
                "details": "It appears that an internal server error has occurred.",
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )
    return JSONResponse(
        {
            "input": number,
            "detection-mode": AUTO_DETECTION if is_auto_detect else MANUAL_DETECTION,
            "country": country_info,
            "number": {**basic_number_info},
            "formats": {**number_formats},
            **number_metadata,
        },
        status_code=HTTPStatus.OK,
    )
