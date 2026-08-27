"""Temperature validation and classification."""

import math

from .models import TemperatureStatus


def validate_temperature(value: float) -> None:
    """Raise ValueError unless *value* is a finite temperature in [-40, 85]."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("temperature must be a number")
    if not math.isfinite(value) or not -40 <= value <= 85:
        raise ValueError("temperature must be between -40 and 85 °C")


def get_temperature_status(value: float) -> TemperatureStatus:
    validate_temperature(value)
    if value >= 35:
        return TemperatureStatus.CRITICAL
    if value >= 30:
        return TemperatureStatus.WARNING
    return TemperatureStatus.NORMAL
