import math

import pytest

from iot.air_quality import MAX_AQI, get_air_quality_status, validate_air_quality
from iot.models import AirQualityStatus

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("value", [0, 50, 100, 150, MAX_AQI])
def test_valid_aqi_is_accepted(value: float) -> None:
    assert validate_air_quality(value) is None


@pytest.mark.parametrize("value", [-1, 500.1, math.inf, math.nan, "good", True])
def test_invalid_aqi_raises_value_error(value: object) -> None:
    with pytest.raises(ValueError):
        get_air_quality_status(value)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("aqi", "expected"),
    [
        (0, AirQualityStatus.GOOD),
        (50, AirQualityStatus.GOOD),
        (51, AirQualityStatus.MODERATE),
        (100, AirQualityStatus.MODERATE),
        (101, AirQualityStatus.UNHEALTHY),
        (150, AirQualityStatus.UNHEALTHY),
        (151, AirQualityStatus.CRITICAL),
        (500, AirQualityStatus.CRITICAL),
    ],
)
def test_air_quality_status_boundaries(aqi: float, expected: AirQualityStatus) -> None:
    assert get_air_quality_status(aqi) is expected
