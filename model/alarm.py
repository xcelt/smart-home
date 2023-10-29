from microservice import Microservice


class Alarm:
    alarmList = list()

    def __init__(self, name: str, type: Microservice) -> None:
        self.name = name
        self.type = type
        self.enabled = False
        Alarm.alarmList.append(self)

    def __str__(self) -> str:
        return self.name

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def is_enabled(self):
        return self.enabled

    def get_alarms():
        return Alarm.alarmList

    def display_alarms():
        print(*Alarm.alarmList, sep=", ")

    def enable_all():
        for alarm in Alarm.alarmList:
            if not alarm.enabled:
                alarm.enable()
        print("All alarms enabled.")

    def disable_all():
        for alarm in Alarm.alarmList:
            if alarm.enabled:
                alarm.disable()
        print("All alarms disabled.")
