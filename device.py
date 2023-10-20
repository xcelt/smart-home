import json
import random


class Device:
    def __init__(self, identifier, threshold=50):
        self.identifier = identifier
        self.status = "active" #Or deactive
        self.threshold = threshold

    def activate(self):
        self.status = "active"

    def deactivate(self):
        self.status = "deactive"

    def set_threshold(self, value):
        self.threshold = value

    def get_readings(self):
        return {'identifier':self.identifier, 'status':self.status, 'threshold':self.threshold}


    def __str__(self):
        return str(self.__class__.__name__) + "| " + json.dumps(self.get_readings())


class SmartLight(Device):
    def __init__(self, identifier, threshold=50):
        super().__init__(identifier, threshold)
        self.brightness = 90 #Day time default
        self.switch = 'on'

    def switch_on(self):
        self.switch = 'on'

    def switch_off(self):
        self.switch = 'off'

    def get_value(self):
        return self.brightness

    def set_value(self, value):
        if value >= 100:
            self.brightness = 100
        elif value < 0:
            self.brightness = 0
        else:
            self.brightness = value

    def get_readings(self):
        pareadings = super().get_readings()
        pareadings.update({'switch': self.switch, 'brightness': self.brightness})
        return pareadings

    def sense(self, simval=None):
        # Simulate it
        if simval is None:
            self.set_value(self.get_value() + random.randint(-2, 2))
        else:
            self.set_value(simval)

        if self.status=="active" and self.switch=="on" and self.brightness >= self.threshold:
            print("Threshold exceeded. Switching light off")
            self.switch_off()
        if self.status == "active" and self.switch == "off" and self.brightness < self.threshold:
            print("Threshold subceeded. Switching light on")
            self.switch_on()

class MotionSensor(Device):
    def __init__(self, identifier, threshold=5):
        super().__init__(identifier, threshold)
        self.motion = 0
        self.switch = 'on'

    def alert_on(self):
        self.switch = 'on'

    def alert_off(self):
        self.switch = 'off'

    def set_value(self, value):
        if value > 10:
            self.motion = 10
        elif value < 0:
            self.motion = 0
        else:
            self.motion = value

    def get_value(self):
        return self.motion

    def get_readings(self):
        pareadings = super().get_readings()
        pareadings.update({'switch': self.switch, 'motion': self.motion})
        return pareadings

    def sense(self, simval=None):
        # Simulate it
        if simval is None:
            self.set_value(self.get_value() + random.randint(-1, 1))
        else:
            self.set_value(simval)

        if self.status=="active" and self.switch=="on" and self.motion >= self.threshold:
            print("Motion detected!")



class SmartLock(Device):
    def __init__(self, identifier):
        super().__init__(identifier)
        self.switch = 'on'

    def lock(self):
        self.switch = 'on'

    def unlock(self):
        self.switch = 'off'

    def get_readings(self):
        pareadings = super().get_readings()
        pareadings.update({'switch': self.switch})
        return pareadings

class Thermostat(Device):
    def __init__(self, identifier, threshold=23):
        super().__init__(identifier, threshold)
        self.temp = 15.0
        self.switch = 'on'

    def switch_on(self):
        self.switch = 'on'

    def switch_off(self):
        self.switch = 'off'

    def set_value(self, value):
        self.temp = value

    def get_value(self):
        return self.temp

    def get_readings(self):
        pareadings = super().get_readings()
        pareadings.update({'switch': self.switch, 'temp': self.temp})
        return pareadings

    def sense(self, simval=None):
        # Simulate it
        if simval is None:
            self.set_value(self.get_value() + float(random.randint(-1, 1))/10)
        else:
            self.set_value(simval)

        if self.status=="active" and self.switch=="on" and self.temp >= self.threshold:
            print("Temperature threshold exceeded. Capping temperature at threshold")
            self.temp = self.threshold




