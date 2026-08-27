"""Hardware boundaries. Concrete hardware adapters would implement ``read``."""

from abc import ABC, abstractmethod

from .models import MeasurementType


class Sensor(ABC):
    measurement_type: MeasurementType

    @abstractmethod
    def read(self) -> float:
        """Return one raw measurement."""


class TemperatureSensor(Sensor):
    measurement_type = MeasurementType.TEMPERATURE


class HumiditySensor(Sensor):
    measurement_type = MeasurementType.HUMIDITY


class AirQualitySensor(Sensor):
    measurement_type = MeasurementType.AIR_QUALITY
