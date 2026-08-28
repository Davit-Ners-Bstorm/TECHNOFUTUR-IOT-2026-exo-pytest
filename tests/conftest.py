from unittest.mock import Mock

import pytest

from iot.alerts import AlertService, Notifier
from iot.controller import IoTController
from iot.device import IoTDevice
from iot.models import MeasurementType
from iot.sensors import Sensor


@pytest.fixture
def temperature_sensor() -> Mock:
    sensor = Mock(spec=Sensor)
    sensor.measurement_type = MeasurementType.TEMPERATURE
    sensor.read.return_value = 22.5
    return sensor


@pytest.fixture
def humidity_sensor() -> Mock:
    sensor = Mock(spec=Sensor)
    sensor.measurement_type = MeasurementType.HUMIDITY
    sensor.read.return_value = 45
    return sensor


@pytest.fixture
def air_quality_sensor() -> Mock:
    sensor = Mock(spec=Sensor)
    sensor.measurement_type = MeasurementType.AIR_QUALITY
    sensor.read.return_value = 42
    return sensor


@pytest.fixture
def notifier() -> Mock:
    return Mock(spec=Notifier)


@pytest.fixture
def alert_service(notifier: Mock) -> AlertService:
    return AlertService(notifier)


@pytest.fixture
def normal_device(temperature_sensor: Mock) -> IoTDevice:
    return IoTDevice("SENSOR-001", "Living room", temperature_sensor, 80)


@pytest.fixture
def controller(alert_service: AlertService) -> IoTController:
    return IoTController(alert_service)
