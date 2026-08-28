import math

import pytest

from iot.humidity import get_humidity_status, validate_humidity
from iot.models import HumidityStatus

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("value", [0, 30, 70, 100, 45.5])
def test_valid_humidity_is_accepted(value: float) -> None:
    assert validate_humidity(value) is None


@pytest.mark.parametrize("value", [-0.1, 100.1, math.inf, math.nan, None, False])
def test_invalid_humidity_raises_value_error(value: object) -> None:
    with pytest.raises(ValueError):
        get_humidity_status(value)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("humidity", "expected"),
    [
        (0, HumidityStatus.LOW),
        (29.9, HumidityStatus.LOW),
        (30, HumidityStatus.NORMAL),
        (70, HumidityStatus.NORMAL),
        (70.1, HumidityStatus.HIGH),
        (100, HumidityStatus.HIGH),
    ],
)
def test_humidity_status_boundaries(humidity: float, expected: HumidityStatus) -> None:
    assert get_humidity_status(humidity) is expected
