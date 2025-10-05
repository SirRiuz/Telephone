# Python
import re


# Detection modes
MANUAL_DETECTION = "by-code"
AUTO_DETECTION = "auto-detect"

PHONE_INDICATIVE = "+"

PHONE_REGEX = re.compile(r"^\+?(?:\(\d+\)|\d+)(?:[ -]?(?:\(\d+\)|\d+))*$")
