import math

import pytest

from iot.models import TemperatureStatus
from iot.temperature import get_temperature_status, validate_temperature

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("value", [-40, 0, 85, 22.5])
def test_valid_temperature_is_accepted(value: float) -> None:
    assert validate_temperature(value) is None


@pytest.mark.parametrize("value", [-40.1, 85.1, math.inf, math.nan, "20", True])
def test_invalid_temperature_raises_value_error(value: object) -> None:
    with pytest.raises(ValueError):
        get_temperature_status(value)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("temperature", "expected"),
    [
        (-40, TemperatureStatus.NORMAL),
        (29.9, TemperatureStatus.NORMAL),
        (30, TemperatureStatus.WARNING),
        (34.9, TemperatureStatus.WARNING),
        (35, TemperatureStatus.CRITICAL),
        (85, TemperatureStatus.CRITICAL),
    ],
)
def test_temperature_status_boundaries(temperature: float, expected: TemperatureStatus) -> None:
    assert get_temperature_status(temperature) is expected


def test_temperature_status_boundary_35() -> None:
    assert get_temperature_status(35) is TemperatureStatus.CRITICAL
