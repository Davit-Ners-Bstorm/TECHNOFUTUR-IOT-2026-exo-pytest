"""Shared enumerations used by the monitor."""

from enum import Enum


class MeasurementType(str, Enum):
    TEMPERATURE = "TEMPERATURE"
    HUMIDITY = "HUMIDITY"
    AIR_QUALITY = "AIR_QUALITY"


class TemperatureStatus(str, Enum):
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class HumidityStatus(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


class AirQualityStatus(str, Enum):
    GOOD = "GOOD"
    MODERATE = "MODERATE"
    UNHEALTHY = "UNHEALTHY"
    CRITICAL = "CRITICAL"


class BatteryStatus(str, Enum):
    CRITICAL = "CRITICAL"
    LOW = "LOW"
    OK = "OK"


class DeviceHealth(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    NO_POWER = "NO_POWER"
    OFFLINE = "OFFLINE"
