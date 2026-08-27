"""Alert decisions and the notification boundary."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from .models import BatteryStatus


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        """Deliver an alert message."""


def should_send_alert(measurement_status: Enum, battery_status: BatteryStatus) -> bool:
    return measurement_status.value == "CRITICAL" or battery_status is BatteryStatus.CRITICAL


def build_alert_message(
    device_id: str,
    measurement_status: Enum,
    battery_status: BatteryStatus,
) -> str:
    reasons: list[str] = []
    if measurement_status.value == "CRITICAL":
        reasons.append(f"measurement={measurement_status.value}")
    if battery_status is BatteryStatus.CRITICAL:
        reasons.append(f"battery={battery_status.value}")
    return f"ALERT {device_id}: " + ", ".join(reasons)


@dataclass
class AlertService:
    notifier: Notifier

    def process(self, device_id: str, measurement_status: Enum, battery_status: BatteryStatus) -> bool:
        """Send at most one alert and return whether one was sent."""
        if not should_send_alert(measurement_status, battery_status):
            return False
        self.notifier.send(build_alert_message(device_id, measurement_status, battery_status))
        return True
