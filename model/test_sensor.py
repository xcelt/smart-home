import pytest
from sensor import Sensor


@pytest.fixture
def initialise_sensors():
    motionSensor = Sensor(name="Moshi")
    lightSensor = Sensor("Lite")
    temperatureSensor = Sensor("Tempest")


def test_sensor_activate(initialise_sensors):
    assert sensor.activate() == 0 and sensor.active


def test_sensor_deactivate(initialise_sensors):
    assert sensor.deactivate() == 0 and not sensor.active


def test_sensor_is_active(initialise_sensors):
    assert sensor.is_active()


# # TODO
# def test_display_sensors_active(active: bool = True):
#     assert Sensor.display_sensors() == 0
