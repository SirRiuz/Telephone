# Libs
from modules.telephone.types import RegionInfo, BasicPhoneNumberInfo


def mask_phone(number) -> str:
    """
    Se encarga de enmascarar un numero de telefono usando los asteriscos
    """
    n = "".join(c for c in number if c.isdigit())
    return number[0] + n[:3] + "*" * (len(n) - 5) + n[-2:] if len(n) > 5 else n[0] + "*" * (len(n) - 1)


def get_country_info_by_code_region(code_region: str) -> RegionInfo:
    """
    Retrieves country information based on its ISO alpha-2 code.
    Only the country code is needed to get details like
    name, capital, flag, timezone, and calling code.
    """

    import pycountry
    import flag as flags
    from countryinfo import CountryInfo
    from phonenumbers import country_code_for_region

    flag = flags.flag(code_region if code_region else "Unknow")
    country = pycountry.countries.get(alpha_2=code_region).name

    info = CountryInfo(country).info()
    capital = info.get("capital")
    timezone = info.get("timezones", [None])[0]

    calling_code = country_code_for_region(code_region)

    return RegionInfo(
        flag=flag,
        name=country,
        capital=capital,
        code=code_region,
        timezones=timezone,
        calling_code=f"+{calling_code}",
    )


def get_basic_phone_number_info(
    calling_code: str,
    number: str,
) -> BasicPhoneNumberInfo:
    calling_code = f"+{calling_code}"
    full_number = f"{calling_code} {number}"
    masked_phone = f"{calling_code} {mask_phone(number)}"
    return BasicPhoneNumberInfo(
        masked=masked_phone,
        full=full_number,
        local=number,
    )


def get_formats(number: str, code_region: str) -> dict[str, str]:

    import phonenumbers
    from phonenumbers import PhoneNumberFormat

    parsed = phonenumbers.parse(number, code_region)
    return {
        "E.164": phonenumbers.format_number(parsed, PhoneNumberFormat.E164),
        "RFC3966": phonenumbers.format_number(parsed, PhoneNumberFormat.RFC3966),
        "international": phonenumbers.format_number(parsed, PhoneNumberFormat.INTERNATIONAL),
        "national": phonenumbers.format_number(parsed, PhoneNumberFormat.NATIONAL),
    }
