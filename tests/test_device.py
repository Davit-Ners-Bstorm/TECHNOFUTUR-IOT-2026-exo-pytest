from unittest.mock import Mock

import pytest

from iot.device import BatteryEmptyError, DeviceOfflineError, IoTDevice
from iot.models import DeviceHealth

pytestmark = pytest.mark.unit


def test_read_sensor_returns_hardware_value(normal_device: IoTDevice, temperature_sensor: Mock) -> None:
    assert normal_device.read_sensor() == 22.5
    temperature_sensor.read.assert_called_once_with()


def test_offline_device_raises_and_does_not_read_sensor(
    normal_device: IoTDevice, temperature_sensor: Mock
) -> None:
    normal_device.set_online(False)
    with pytest.raises(DeviceOfflineError, match="SENSOR-001"):
        normal_device.read_sensor()
    temperature_sensor.read.assert_not_called()


def test_empty_battery_raises_and_does_not_read_sensor(
    normal_device: IoTDevice, temperature_sensor: Mock
) -> None:
    normal_device.update_battery(0)
    with pytest.raises(BatteryEmptyError):
        normal_device.read_sensor()
    temperature_sensor.read.assert_not_called()


def test_sensor_exception_is_propagated(normal_device: IoTDevice, temperature_sensor: Mock) -> None:
    temperature_sensor.read.side_effect = RuntimeError("I2C timeout")
    with pytest.raises(RuntimeError, match="I2C timeout"):
        normal_device.read_sensor()


@pytest.mark.parametrize(
    ("online", "battery", "expected"),
    [
        (True, 80, DeviceHealth.HEALTHY),
        (True, 25, DeviceHealth.DEGRADED),
        (True, 0, DeviceHealth.NO_POWER),
        (False, 80, DeviceHealth.OFFLINE),
        (False, 0, DeviceHealth.OFFLINE),
    ],
)
def test_health_status(
    normal_device: IoTDevice, online: bool, battery: float, expected: DeviceHealth
) -> None:
    normal_device.set_online(online)
    normal_device.update_battery(battery)
    assert normal_device.get_health_status() is expected


@pytest.mark.parametrize("level", [-1, 101])
def test_update_battery_rejects_invalid_level(normal_device: IoTDevice, level: float) -> None:
    with pytest.raises(ValueError):
        normal_device.update_battery(level)


def test_set_online_requires_bool(normal_device: IoTDevice) -> None:
    with pytest.raises(TypeError):
        normal_device.set_online(1)  # type: ignore[arg-type]


@pytest.mark.parametrize(("device_id", "name"), [("", "Room"), ("  ", "Room"), ("D1", "")])
def test_device_requires_identity(device_id: str, name: str, temperature_sensor: Mock) -> None:
    with pytest.raises(ValueError):
        IoTDevice(device_id, name, temperature_sensor, 50)


@pytest.mark.hardware
@pytest.mark.skip(reason="demonstration: requires a real sensor adapter")
def test_real_sensor_adapter() -> None:
    assert False
