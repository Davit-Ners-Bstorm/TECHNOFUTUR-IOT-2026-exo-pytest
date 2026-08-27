"""Orchestration of a fleet of simulated devices."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

from .air_quality import get_air_quality_status
from .alerts import AlertService
from .battery import get_battery_status
from .device import BatteryEmptyError, DeviceOfflineError, IoTDevice
from .humidity import get_humidity_status
from .models import MeasurementType
from .temperature import get_temperature_status

Classifier = Callable[[float], Enum]


@dataclass
class IoTController:
    alert_service: AlertService | None = None
    _devices: dict[str, IoTDevice] = field(default_factory=dict, init=False)

    def register_device(self, device: IoTDevice) -> None:
        if device.device_id in self._devices:
            raise ValueError(f"device {device.device_id} is already registered")
        self._devices[device.device_id] = device

    def remove_device(self, device_id: str) -> IoTDevice:
        if device_id not in self._devices:
            raise KeyError(device_id)
        return self._devices.pop(device_id)

    def get_device(self, device_id: str) -> IoTDevice:
        if device_id not in self._devices:
            raise KeyError(device_id)
        return self._devices[device_id]

    def collect_readings(self) -> dict[str, dict[str, Any]]:
        report: dict[str, dict[str, Any]] = {}
        for device_id, device in self._devices.items():
            try:
                value = device.read_sensor()
                status = self._classifier_for(device.sensor.measurement_type)(value)
                battery_status = get_battery_status(device.battery_level)
                alert_sent = False
                if self.alert_service is not None:
                    alert_sent = self.alert_service.process(device_id, status, battery_status)
                report[device_id] = {
                    "value": value,
                    "status": status.value,
                    "battery": device.battery_level,
                    "battery_status": battery_status.value,
                    "alert_sent": alert_sent,
                }
            except DeviceOfflineError:
                report[device_id] = {"error": "DEVICE_OFFLINE"}
            except BatteryEmptyError:
                report[device_id] = {"error": "BATTERY_EMPTY"}
            except ValueError as error:
                report[device_id] = {"error": "INVALID_READING", "detail": str(error)}
            except Exception as error:
                report[device_id] = {"error": "SENSOR_FAILURE", "detail": str(error)}
        return report

    @staticmethod
    def _classifier_for(measurement_type: MeasurementType) -> Classifier:
        classifiers: dict[MeasurementType, Classifier] = {
            MeasurementType.TEMPERATURE: get_temperature_status,
            MeasurementType.HUMIDITY: get_humidity_status,
            MeasurementType.AIR_QUALITY: get_air_quality_status,
        }
        try:
            return classifiers[measurement_type]
        except KeyError as error:
            raise ValueError(f"unsupported measurement type: {measurement_type}") from error
