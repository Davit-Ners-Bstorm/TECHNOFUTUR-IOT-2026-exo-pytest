"""The central IoT device entity."""

from dataclasses import dataclass

from .battery import get_battery_status, validate_battery
from .models import BatteryStatus, DeviceHealth
from .sensors import Sensor


class DeviceOfflineError(RuntimeError):
    """Raised when an offline device is read."""


class BatteryEmptyError(RuntimeError):
    """Raised when a device has no power left."""


@dataclass
class IoTDevice:
    device_id: str
    name: str
    sensor: Sensor
    battery_level: float
    online: bool = True

    def __post_init__(self) -> None:
        if not self.device_id.strip():
            raise ValueError("device_id cannot be empty")
        if not self.name.strip():
            raise ValueError("name cannot be empty")
        validate_battery(self.battery_level)

    def read_sensor(self) -> float:
        if not self.online:
            raise DeviceOfflineError(f"device {self.device_id} is offline")
        if self.battery_level == 0:
            raise BatteryEmptyError(f"device {self.device_id} has no battery")
        return self.sensor.read()

    def set_online(self, online: bool) -> None:
        if not isinstance(online, bool):
            raise TypeError("online must be a bool")
        self.online = online

    def update_battery(self, level: float) -> None:
        validate_battery(level)
        self.battery_level = level

    def get_health_status(self) -> DeviceHealth:
        if not self.online:
            return DeviceHealth.OFFLINE
        if self.battery_level == 0:
            return DeviceHealth.NO_POWER
        if get_battery_status(self.battery_level) is not BatteryStatus.OK:
            return DeviceHealth.DEGRADED
        return DeviceHealth.HEALTHY
