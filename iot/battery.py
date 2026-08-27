"""Battery-level validation and classification."""

import math

from .models import BatteryStatus


def validate_battery(level: float) -> None:
    if isinstance(level, bool) or not isinstance(level, (int, float)):
        raise ValueError("battery level must be a number")
    if not math.isfinite(level) or not 0 <= level <= 100:
        raise ValueError("battery level must be between 0 and 100 %")


def get_battery_status(level: float) -> BatteryStatus:
    validate_battery(level)
    if level <= 10:
        return BatteryStatus.CRITICAL
    if level <= 25:
        return BatteryStatus.LOW
    return BatteryStatus.OK
