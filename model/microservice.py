from enum import Enum


class Microservice(Enum):
    SENSOR = 1
    THERMOSTAT = 2
    CAMERA = 3
    LIGHT = 4
    SMART_LOCK = 5

    def __str__(self) -> str:
        return self.name.capitalize()