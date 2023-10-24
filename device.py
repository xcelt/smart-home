'''
This module contains the classes for the IoT devices (currentl Device, from which MotionSensor, SmartLight, SmartLock and Thermostat inherit).
Possible to seamlessly create other devices by inherting from Device and keeping to the similar structure
'''

import json
import random


class Device:
    """
    The Device class represents a device with an identifier, status (active or deactive), and a threshold value.

    Attributes:
        identifier (str): A unique identifier for the device.
        status (str): The status of the device, can be "active" or "deactive".
        threshold (int): The threshold value for the device's operation.

    Constants:
        THRES_MIN (int): The minimum threshold value allowed.
        THRES_MAX (int): The maximum threshold value allowed.

    Methods:
        __init__(self, identifier, threshold=50):
            Initializes a new Device instance with the given identifier and an optional threshold value.
            If threshold is not provided, it defaults to 50.

        activate(self):
            Activates the device, setting its status to "active."

        deactivate(self):
            Deactivates the device, setting its status to "deactive."

        set_threshold(self, value):
            Sets the threshold value for the device, ensuring it falls within the allowed range [THRES_MIN, THRES_MAX].

        get_readings(self):
            Returns a dictionary containing information about the device, including its identifier, status, and threshold.

        __str__(self):
            Returns a string representation of the Device, including its class name and device readings in JSON format.

    Example usage:
        device = Device("device001", 60)
        print(device.get_readings())  # {'identifier': 'example_device', 'status': 'active', 'threshold': 60}
    """
    def __init__(self, identifier, threshold=50):
        """Initialize a new Device instance."""
        self.identifier = identifier
        self.status = "active" #Or deactive
        self.set_threshold(threshold)


    def activate(self):
        """Activate the device, setting its status to 'active'."""
        self.status = "active"

    def deactivate(self):
        """Deactivate the device, setting its status to 'deactive'."""
        self.status = "deactive"

    def set_threshold(self, value):
        """
        Set the threshold value for the device, ensuring it falls within the allowed range [THRES_MIN, THRES_MAX].
        If it falls above THRES_MAX, it sets it to THRES_MAX; same for THRES_MIN

                Args:
                    value (int): The threshold value to set.
                """
        if value > self.THRES_MAX:
            self.threshold = self.THRES_MAX
        elif value < self.THRES_MIN:
            self.threshold = self.THRES_MIN
        else:
            self.threshold = value

    def get_readings(self):
        """
        Retrieve and return information about the device.

        Returns:
            dict: A dictionary containing 'identifier', 'status', and 'threshold' keys.
        """
        return {'identifier':self.identifier, 'status':self.status, 'threshold':self.threshold}


    def __str__(self):
        """
        Get a string representation of the Device.

        Returns:
            str: A string containing the class name and device readings in JSON format.
        """
        return str(self.__class__.__name__) + "| " + json.dumps(self.get_readings())


class SmartLight(Device):
    """
        The SmartLight class represents a controllable light device that inherits from the Device class.
        It includes features like brightness control and the ability to sense and respond to light levels.
        For this device, switch_on and switch_off represent actually switching on/off the light,
        and activation/deactivation represent whether or not the light will automatically go on/off depending
        on the brightness level


        Attributes:
            identifier (str): A unique identifier for the smart light.
            threshold (int): The brightness threshold value for automatic light control.
            brightness (int): The current brightness level of the light.
            switch (str): The switch status ('on' or 'off').

        Methods:
            __init__(self, identifier, threshold=50):
                Initializes a new SmartLight instance with the given identifier and an optional threshold value.
                If threshold is not provided, it defaults to 50.

            switch_on(self):
                Turns the light on by setting the switch status to 'on'.

            switch_off(self):
                Turns the light off by setting the switch status to 'off'.

            get_value(self):
                Returns the current brightness level of the light.

            set_value(self, value):
                Sets the brightness level of the light, ensuring it falls within the range [0, 100].

            get_readings(self):
                Returns a dictionary containing information about the smart light, including its identifier, status, threshold, switch, and brightness.

            sense(self, simval=None):
                Simulates the smart light's ability to sense and respond to light levels. It adjusts brightness and may turn the light on or off based on thresholds.

        Example usage:
            light = SmartLight("Light001", 60)
            light.sense()
        """
    def __init__(self, identifier, threshold=50):
        """Initialize a new SmartLight instance."""
        self.THRES_MAX = 100
        self.THRES_MIN = 0
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
        """
        Set the brightness level of the light, ensuring it falls within the allowed range [0, 100].

        Args:
            value (int): The brightness level to set.
        """
        if value >= 100:
            self.brightness = 100
        elif value < 0:
            self.brightness = 0
        else:
            self.brightness = value

    def get_readings(self):
        """
        Get information about the smart light, including its identifier, status, threshold, switch, and brightness.

        Returns:
            dict: A dictionary containing device information.
        """
        pareadings = super().get_readings()
        pareadings.update({'switch': self.switch, 'brightness': self.brightness})
        return pareadings

    def sense(self, simval=None):
        """
        Simulate the smart light's ability to sense and respond to light levels.
        It adjusts brightness and may turn the light on or off based on thresholds.

        Args:
            simval (int): An optional simulated light level; if not provided, it will generate and use one.
        """

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
    """
        The MotionSensor class represents a sensor device that detects motion. It inherits from the Device class
        and includes motion detection and a switch to control its operation. For this device,
        switch_on/off specifies whether it should start/stop sensing completely

        Attributes:
            identifier (str): A unique identifier for the motion sensor.
            threshold (int): The motion detection threshold value for triggering alerts.
            motion (int): The current motion level detected by the sensor.
            switch (str): The switch status ('on' or 'off').

        Methods:
            __init__(self, identifier, threshold=5):
                Initializes a new MotionSensor instance with the given identifier and an optional threshold value.
                If threshold is not provided, it defaults to 5.

            switch_on(self):
                Turns the motion sensor on by setting the switch status to 'on'.

            switch_off(self):
                Turns the motion sensor off by setting the switch status to 'off'.

            set_value(self, value):
                Sets the motion level detected by the sensor, ensuring it falls within the allowed range [0, 10].

            get_value(self):
                Returns the current motion level detected by the sensor.

            get_readings(self):
                Returns a dictionary containing information about the motion sensor, including its identifier, status, threshold, switch, and motion level.

            sense(self, simval=None):
                Simulates the motion sensor's ability to sense motion and trigger alerts based on the defined threshold.

            Example usage:
            sensor = MotionSensor("motion005", 7)
            sensor.sense()
        """
    def __init__(self, identifier, threshold=5):
        """Initialize a new MotionSensor instance."""
        self.THRES_MAX = 10
        self.THRES_MIN = 0
        super().__init__(identifier, threshold)
        self.motion = 0
        self.switch = 'on'


    def switch_on(self):
        self.switch = 'on'

    def switch_off(self):
        self.switch = 'off'

    def set_value(self, value):
        """
                Set the motion level detected by the sensor, ensuring it falls within the allowed range [0, 10].

                Args:
                    value (int): The motion level to set.
                """
        if value > 10:
            self.motion = 10
        elif value < 0:
            self.motion = 0
        else:
            self.motion = value

    def get_value(self):
        """Get the current motion level detected by the sensor."""
        return self.motion

    def get_readings(self):
        """
        Get information about the motion sensor, including its identifier, status, threshold, switch, and motion level.

        Returns:
            dict: A dictionary containing device information.
        """
        pareadings = super().get_readings()
        pareadings.update({'switch': self.switch, 'motion': self.motion})
        return pareadings

    def sense(self, simval=None):
        """
        Simulate the motion sensor's ability to sense motion and trigger alerts based on the defined threshold.

        Args:
            simval (int): An optional simulated motion level or if not specified it generates
        """

        #If the switch is off, don't sense
        if self.switch == "off":
            return

        if simval is None:
            self.set_value(self.get_value() + random.randint(-1, 1))
        else:
            self.set_value(simval)

        if self.status=="active" and self.motion >= self.threshold:
            print("Motion detected!")



class SmartLock(Device):
    """
    The SmartLock class represents a lock device that inherits from the Device class. It can be used to lock or unlock access.
    This device doesn't have any sensor.

    Attributes:
        identifier (str): A unique identifier for the smart lock.
        switch (str): The lock switch status ('on' or 'off').

    Methods:
        __init__(self, identifier):
            Initializes a new SmartLock instance with the given identifier.

        lock(self):
            Locks the smart lock, setting the switch status to 'on', but only if the device is active.

        unlock(self):
            Unlocks the smart lock, setting the switch status to 'off', but only if the device is active.

        get_readings(self):
            Returns a dictionary containing information about the smart lock, including its identifier and switch status.

        Example usage:
        lock = SmartLock("lock05")
        lock.lock()
    """
    def __init__(self, identifier):
        """Initialize a new SmartLock instance."""
        self.THRES_MAX = 0
        self.THRES_MIN = 0
        super().__init__(identifier)
        self.switch = 'on'


    def lock(self):
        """
        Lock the smart lock by setting the switch status to 'on' if the device is active.
        """
        if self.status == 'deactive':
            return
        self.switch = 'on'

    def unlock(self):
        """
        Unlock the smart lock by setting the switch status to 'off' if the device is active.
        """
        if self.status == 'deactive':
            return
        self.switch = 'off'

    def get_readings(self):
        """
        Get information about the smart lock, including its identifier and switch status.

        Returns:
            dict: A dictionary containing device information.
        """
        pareadings = super().get_readings()
        pareadings.update({'switch': self.switch})
        return pareadings

class Thermostat(Device):
    """
        The Thermostat class represents a device for controlling temperature. It inherits from the Device class.

        Attributes:
            identifier (str): A unique identifier for the thermostat.
            threshold (int): The temperature threshold value for controlling the thermostat.
            temp (float): The current temperature setpoint.
            switch (str): The switch status ('on' or 'off').

        Methods:
            __init__(self, identifier, threshold=23):
                Initializes a new Thermostat instance with the given identifier and an optional threshold value.
                If threshold is not provided, it defaults to 23.

            switch_on(self):
                Turns the thermostat on by setting the switch status to 'on'.

            switch_off(self):
                Turns the thermostat off by setting the switch status to 'off'.

            set_value(self, value):
                Sets the temperature setpoint for the thermostat.

            get_value(self):
                Returns the current temperature setpoint of the thermostat.

            get_readings(self):
                Returns a dictionary containing information about the thermostat, including its identifier, status, threshold, switch, and temperature setpoint.

            sense(self, simval=None):
                Simulates the thermostat's ability to sense and adjust the temperature based on the defined threshold.

            Example usage:
            thermostat = Thermostat("therm22", 25)
            thermostat.sense()
        """
    def __init__(self, identifier, threshold=23):
        """Initialize a new Thermostat instance."""
        self.THRES_MAX = 40
        self.THRES_MIN = 0
        super().__init__(identifier, threshold)
        self.temp = 15.0
        self.switch = 'on'


    def switch_on(self):
        self.switch = 'on'

    def switch_off(self):
        self.switch = 'off'

    def set_value(self, value):
        """
        Set the temperature setpoint for the thermostat.

        Args:
            value (float): The temperature setpoint to set.
        """
        self.temp = value

    def get_value(self):
        """Get the current temperature setpoint of the thermostat."""
        return self.temp

    def get_readings(self):
        """
        Get information about the thermostat, including its identifier, status, threshold, switch, and temperature setpoint.

        Returns:
            dict: A dictionary containing device information.
        """
        pareadings = super().get_readings()
        pareadings.update({'switch': self.switch, 'temp': self.temp})
        return pareadings

    def sense(self, simval=None):
        """
        Simulate the thermostat's ability to sense and adjust the temperature based on the defined threshold.

        Args:
            simval (float): An optional simulated temperature setpoint.
        """
        # Simulate it

        #If the switch is off, don't sense
        if self.switch == "off":
            return

        if simval is None:
            self.set_value(self.get_value() + round(float(random.randint(-1, 1))/10,1))
        else:
            self.set_value(simval)

        if self.status=="active" and self.temp >= self.threshold:
            print("Temperature threshold exceeded. Capping temperature at threshold")
            self.temp = self.threshold


#Some code I used to test the devices; not used.
# if __name__ == "__main__":
#     s1 = SmartLock("sl1")
#     s1.set_threshold(-1)
#     print(s1.threshold)
#
#     print("Light")
#     s2 = SmartLight("slt1",120)
#     print(s2.threshold)
#     s2.set_threshold(120)
#     print(s2.threshold)
#     s2.set_threshold(-20)
#     print(s2.threshold)
#     s2.set_threshold(40)
#     print(s2.threshold)
#     print("Motion")
#     s3 = Thermostat("m",50)
#     print(s3.threshold)
#     s3.set_threshold(50)
#     print(s3.threshold)
#     s3.set_threshold(-1)
#     print(s3.threshold)
#     s3.set_threshold(3)
#     print(s3.threshold)
#     s3.sense()

