import math

import pytest

from iot.battery import get_battery_status, validate_battery
from iot.models import BatteryStatus

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("level", [0, 10, 25, 100, 50.5])
def test_valid_battery_is_accepted(level: float) -> None:
    assert validate_battery(level) is None


@pytest.mark.parametrize("level", [-0.1, 100.1, math.inf, math.nan, None, True])
def test_invalid_battery_raises_value_error(level: object) -> None:
    with pytest.raises(ValueError):
        get_battery_status(level)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("level", "expected"),
    [
        (0, BatteryStatus.CRITICAL),
        (10, BatteryStatus.CRITICAL),
        (11, BatteryStatus.LOW),
        (25, BatteryStatus.LOW),
        (26, BatteryStatus.OK),
        (100, BatteryStatus.OK),
    ],
)
def test_battery_status_boundaries(level: float, expected: BatteryStatus) -> None:
    assert get_battery_status(level) is expected
