from unittest.mock import Mock

import pytest

from iot.alerts import AlertService, build_alert_message, should_send_alert
from iot.models import AirQualityStatus, BatteryStatus, TemperatureStatus

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("measurement", "battery", "expected"),
    [
        (TemperatureStatus.NORMAL, BatteryStatus.OK, False),
        (TemperatureStatus.WARNING, BatteryStatus.LOW, False),
        (TemperatureStatus.CRITICAL, BatteryStatus.OK, True),
        (AirQualityStatus.CRITICAL, BatteryStatus.OK, True),
        (TemperatureStatus.NORMAL, BatteryStatus.CRITICAL, True),
    ],
)
def test_should_send_alert(measurement: object, battery: BatteryStatus, expected: bool) -> None:
    assert should_send_alert(measurement, battery) is expected  # type: ignore[arg-type]


def test_build_alert_message_combines_both_reasons() -> None:
    message = build_alert_message("SENSOR-7", TemperatureStatus.CRITICAL, BatteryStatus.CRITICAL)
    assert message == "ALERT SENSOR-7: measurement=CRITICAL, battery=CRITICAL"


def test_alert_service_sends_exact_message(notifier: Mock) -> None:
    service = AlertService(notifier)
    assert service.process("SENSOR-1", TemperatureStatus.CRITICAL, BatteryStatus.OK) is True
    notifier.send.assert_called_once_with("ALERT SENSOR-1: measurement=CRITICAL")


def test_alert_service_does_not_send_for_normal_state(notifier: Mock) -> None:
    service = AlertService(notifier)
    assert service.process("SENSOR-1", TemperatureStatus.NORMAL, BatteryStatus.OK) is False
    notifier.send.assert_not_called()


def test_alert_service_sends_only_once_when_two_reasons_exist(notifier: Mock) -> None:
    service = AlertService(notifier)
    service.process("SENSOR-1", TemperatureStatus.CRITICAL, BatteryStatus.CRITICAL)
    notifier.send.assert_called_once()
