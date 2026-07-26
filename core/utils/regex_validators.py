"""
Regex-based validators used across the app (crop names, quality grades,
phone numbers, CSV row sanity checks).
"""

import re


CROP_NAME_PATTERN = re.compile(r"^[A-Za-z\s\(\)\-]{2,80}$")

QUALITY_PATTERN = re.compile(
    r"^(FAQ|Grade[- ]?[ABC]|Premium|Standard|Medium|Local)$",
    re.IGNORECASE
)

PHONE_PATTERN = re.compile(r"^[6-9]\d{9}$")

PRICE_PATTERN = re.compile(r"^\d+(\.\d{1,2})?$")


class ValidationError(Exception):
    """Raised when input fails a regex validation rule."""


def validate_crop_name(name: str) -> str:
    """
    Validates crop name.
    Allows Agmarknet names like Ridgeguard(Tori).
    """

    name = (name or "").strip()

    if not CROP_NAME_PATTERN.match(name):
        raise ValidationError(
            "Crop name must contain valid characters."
        )

    return name.title()



def validate_quality(quality: str) -> str:
    """
    Validates quality grades.
    """

    quality = (quality or "").strip()

    if not QUALITY_PATTERN.match(quality):
        raise ValidationError(
            "Quality must be one of: FAQ, Grade-A/B/C, Premium, Standard, Medium, Local."
        )

    return quality.title()



def validate_phone(phone: str) -> str:

    phone = (phone or "").strip()

    if not PHONE_PATTERN.match(phone):
        raise ValidationError(
            "Enter a valid 10-digit Indian mobile number."
        )

    return phone



def validate_price(value: str) -> float:

    value = str(value).strip()

    if not PRICE_PATTERN.match(value):
        raise ValidationError(
            "Price must be a positive number with up to 2 decimal places."
        )

    return float(value)



def is_safe_search_query(query: str) -> bool:
    """
    Blocks obvious injection/junk characters.
    """

    return bool(
        re.match(
            r"^[A-Za-z0-9\s\-]{1,50}$",
            (query or "").strip()
        )
    )