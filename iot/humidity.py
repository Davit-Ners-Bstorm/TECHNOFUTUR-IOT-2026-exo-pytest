"""Relative-humidity validation and classification."""

import math

from .models import HumidityStatus


def validate_humidity(value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("humidity must be a number")
    if not math.isfinite(value) or not 0 <= value <= 100:
        raise ValueError("humidity must be between 0 and 100 %")


def get_humidity_status(value: float) -> HumidityStatus:
    validate_humidity(value)
    if value < 30:
        return HumidityStatus.LOW
    if value <= 70:
        return HumidityStatus.NORMAL
    return HumidityStatus.HIGH
