"""Run a tiny fleet without real hardware: ``python demo.py``."""

from dataclasses import dataclass
from pprint import pprint

from iot.alerts import AlertService, Notifier
from iot.controller import IoTController
from iot.device import IoTDevice
from iot.models import MeasurementType
from iot.sensors import Sensor


@dataclass
class SimulatedSensor(Sensor):
    measurement_type: MeasurementType
    value: float

    def read(self) -> float:
        return self.value


class ConsoleNotifier(Notifier):
    def send(self, message: str) -> None:
        print(message)


def main() -> None:
    controller = IoTController(AlertService(ConsoleNotifier()))
    controller.register_device(
        IoTDevice(
            "TEMP-001",
            "Training room",
            SimulatedSensor(MeasurementType.TEMPERATURE, 35.2),
            80,
        )
    )
    controller.register_device(
        IoTDevice(
            "AIR-001",
            "Workshop",
            SimulatedSensor(MeasurementType.AIR_QUALITY, 72),
            20,
        )
    )
    pprint(controller.collect_readings(), sort_dicts=False)


if __name__ == "__main__":
    main()
