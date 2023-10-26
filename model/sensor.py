class Sensor:
    sensorList = list()

    def __init__(self, name: str):
        self.name = name
        self.active = True
        Sensor.sensorList.append(self)

    def __str__(self) -> str:
        return self.name

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def is_active(self):
        return self.active

    def display_sensors(active: bool = True):
        if Sensor.sensorList:
            for sensor in Sensor.sensorList:
                if sensor.is_active:
                    print(f"{sensor} is connected.")
        else:
            print("No devices found.")
