from unittest.mock import Mock

import pytest

from iot.controller import IoTController
from iot.device import IoTDevice
from iot.models import MeasurementType

pytestmark = pytest.mark.integration


def test_register_and_get_device(controller: IoTController, normal_device: IoTDevice) -> None:
    controller.register_device(normal_device)
    assert controller.get_device("SENSOR-001") is normal_device


def test_duplicate_device_is_rejected(controller: IoTController, normal_device: IoTDevice) -> None:
    controller.register_device(normal_device)
    with pytest.raises(ValueError, match="already registered"):
        controller.register_device(normal_device)


def test_remove_device_returns_device(controller: IoTController, normal_device: IoTDevice) -> None:
    controller.register_device(normal_device)
    assert controller.remove_device("SENSOR-001") is normal_device
    with pytest.raises(KeyError):
        controller.get_device("SENSOR-001")


@pytest.mark.parametrize("operation", ["get", "remove"])
def test_unknown_device_raises_key_error(controller: IoTController, operation: str) -> None:
    with pytest.raises(KeyError):
        getattr(controller, f"{operation}_device")("UNKNOWN")


def test_collect_temperature_report(controller: IoTController, normal_device: IoTDevice) -> None:
    controller.register_device(normal_device)
    assert controller.collect_readings() == {
        "SENSOR-001": {
            "value": 22.5,
            "status": "NORMAL",
            "battery": 80,
            "battery_status": "OK",
            "alert_sent": False,
        }
    }


def test_collects_multiple_sensor_types(
    controller: IoTController,
    normal_device: IoTDevice,
    humidity_sensor: Mock,
    air_quality_sensor: Mock,
) -> None:
    humidity_sensor.read.return_value = 75
    air_quality_sensor.read.return_value = 120
    controller.register_device(normal_device)
    controller.register_device(IoTDevice("H-1", "Greenhouse", humidity_sensor, 60))
    controller.register_device(IoTDevice("AQ-1", "Workshop", air_quality_sensor, 40))
    report = controller.collect_readings()
    assert report["SENSOR-001"]["status"] == "NORMAL"
    assert report["H-1"]["status"] == "HIGH"
    assert report["AQ-1"]["status"] == "UNHEALTHY"


def test_offline_device_does_not_stop_collection(
    controller: IoTController, normal_device: IoTDevice, humidity_sensor: Mock
) -> None:
    normal_device.set_online(False)
    second = IoTDevice("H-1", "Office", humidity_sensor, 90)
    controller.register_device(normal_device)
    controller.register_device(second)
    report = controller.collect_readings()
    assert report["SENSOR-001"] == {"error": "DEVICE_OFFLINE"}
    assert report["H-1"]["value"] == 45


def test_empty_battery_becomes_report_error(controller: IoTController, normal_device: IoTDevice) -> None:
    normal_device.update_battery(0)
    controller.register_device(normal_device)
    assert controller.collect_readings()["SENSOR-001"] == {"error": "BATTERY_EMPTY"}


def test_hardware_failure_becomes_report_error(
    controller: IoTController, normal_device: IoTDevice, temperature_sensor: Mock
) -> None:
    temperature_sensor.read.side_effect = RuntimeError("disconnected")
    controller.register_device(normal_device)
    result = controller.collect_readings()["SENSOR-001"]
    assert result == {"error": "SENSOR_FAILURE", "detail": "disconnected"}


def test_invalid_reading_becomes_report_error(
    controller: IoTController, normal_device: IoTDevice, temperature_sensor: Mock
) -> None:
    temperature_sensor.read.return_value = 90
    controller.register_device(normal_device)
    result = controller.collect_readings()["SENSOR-001"]
    assert result["error"] == "INVALID_READING"
    assert "-40 and 85" in result["detail"]


def test_critical_reading_sends_alert(
    controller: IoTController, normal_device: IoTDevice, temperature_sensor: Mock, notifier: Mock
) -> None:
    temperature_sensor.read.return_value = 35
    controller.register_device(normal_device)
    result = controller.collect_readings()["SENSOR-001"]
    assert result["alert_sent"] is True
    notifier.send.assert_called_once_with("ALERT SENSOR-001: measurement=CRITICAL")


def test_normal_reading_sends_no_alert(
    controller: IoTController, normal_device: IoTDevice, notifier: Mock
) -> None:
    controller.register_device(normal_device)
    controller.collect_readings()
    notifier.send.assert_not_called()


def test_low_but_not_critical_battery_sends_no_alert(
    controller: IoTController, normal_device: IoTDevice, notifier: Mock
) -> None:
    normal_device.update_battery(20)
    controller.register_device(normal_device)
    result = controller.collect_readings()["SENSOR-001"]
    assert result["battery_status"] == "LOW"
    notifier.send.assert_not_called()


def test_critical_battery_sends_alert(
    controller: IoTController, normal_device: IoTDevice, notifier: Mock
) -> None:
    normal_device.update_battery(10)
    controller.register_device(normal_device)
    controller.collect_readings()
    notifier.send.assert_called_once_with("ALERT SENSOR-001: battery=CRITICAL")


def test_unknown_measurement_type_is_reported(
    controller: IoTController, normal_device: IoTDevice
) -> None:
    normal_device.sensor.measurement_type = "NOISE"
    controller.register_device(normal_device)
    result = controller.collect_readings()["SENSOR-001"]
    assert result["error"] == "INVALID_READING"
    assert "unsupported measurement type" in result["detail"]


@pytest.mark.xfail(reason="optional feature not implemented: rolling averages")
def test_controller_exposes_rolling_average(controller: IoTController) -> None:
    assert controller.get_rolling_average("SENSOR-001") == 22.5  # type: ignore[attr-defined]
