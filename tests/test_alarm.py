import pytest
from microservice import Microservice
from model.alarm import Alarm


@pytest.fixture
def initialise_alarms():
    sensorAlarm = Alarm(name="Senza", type=Microservice.SENSOR)
    thermostatAlarm = Alarm("Thano", Microservice.THERMOSTAT)
    cameraAlarm = Alarm("Cameron", Microservice.CAMERA)
    lightAlarm = Alarm("SmartLightsaber", Microservice.LIGHT)
    smartlockAlarm = Alarm("Sherlock", Microservice.SMART_LOCK)


# def test_microservice():
#     assert len(Microservice) == 5


# def test_alarm():
#     initialise_alarms()
#     alarmList = Alarm.get_alarms()
#     for alarm in alarmList:
#         print(alarm.enabled)
#     Alarm.display_alarms()


def test_alarm_get_alarms(initialise_alarms):
    assert len(Alarm.get_alarms()) == 5


# @pytest.mark.parametrize("", initialise_alarms())
# def test_alarm_enable_all():
#     Alarm.enable_all()
#     for alarm in Alarm.__alarmList:
#         assert alarm.enabled

#     # Alarm.enable_all()
#     # Alarm.disable_all()


# test_alarm()
# test_alarm_enable_all()
