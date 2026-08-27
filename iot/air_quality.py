"""Simplified Air Quality Index rules."""

import math

from .models import AirQualityStatus

MAX_AQI = 500


def validate_air_quality(aqi: float) -> None:
    if isinstance(aqi, bool) or not isinstance(aqi, (int, float)):
        raise ValueError("AQI must be a number")
    if not math.isfinite(aqi) or not 0 <= aqi <= MAX_AQI:
        raise ValueError(f"AQI must be between 0 and {MAX_AQI}")


def get_air_quality_status(aqi: float) -> AirQualityStatus:
    validate_air_quality(aqi)
    if aqi <= 50:
        return AirQualityStatus.GOOD
    if aqi <= 100:
        return AirQualityStatus.MODERATE
    if aqi <= 150:
        return AirQualityStatus.UNHEALTHY
    return AirQualityStatus.CRITICAL
