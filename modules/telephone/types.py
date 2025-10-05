# Python
from dataclasses import dataclass


@dataclass
class RegionInfo:

    name: str
    flag: str
    code: str
    capital: str
    timezones: str
    calling_code: str


@dataclass
class BasicPhoneNumberInfo:

    full: str
    local: str
    masked: str
