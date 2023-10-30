import unittest
import sys
sys.path.append("../")


from model.device import *


class TestDevice(unittest.TestCase):

    def test_initialization(self):
        device = Device("device001", 60)
        self.assertEqual(device.identifier, "device001")
        self.assertEqual(device.status, "active")
        self.assertEqual(device.threshold, 60)

    def test_activation(self):
        device = Device("device001", 60)
        device.activate()
        self.assertEqual(device.status, "active")

    def test_deactivation(self):
        device = Device("device001", 60)
        device.deactivate()
        self.assertEqual(device.status, "inactive")

    def test_threshold_within_range(self):
        device = Device("device001", 60)
        device.set_threshold(75)
        self.assertEqual(device.threshold, 75)

    def test_threshold_above_maximum(self):
        device = Device("device001", 60)
        device.set_threshold(150)
        self.assertEqual(device.threshold, device.thres_max)

    def test_threshold_below_minimum(self):
        device = Device("device001", 60)
        device.set_threshold(-10)
        self.assertEqual(device.threshold, device.thres_min)

    def test_get_readings(self):
        device = Device("device001", 60)
        readings = device.get_readings()
        self.assertEqual(readings['identifier'], "device001")
        self.assertEqual(readings['status'], "active")
        self.assertEqual(readings['threshold'], 60)

    def test_str_representation(self):
        device = Device("device001", 60)
        str_repr = str(device)
        expected_str = 'Device| {"identifier": "device001", "status": "active", "threshold": 60}'
        self.assertEqual(str_repr, expected_str)


class TestSmartLight(unittest.TestCase):

    def test_initialization(self):
        smart_light = SmartLight("light001", 60)
        self.assertEqual(smart_light.identifier, "light001")
        self.assertEqual(smart_light.status, "active")
        self.assertEqual(smart_light.threshold, 60)
        self.assertEqual(smart_light.brightness, 90)
        self.assertEqual(smart_light.switch, "on")

    def test_switch_on(self):
        smart_light = SmartLight("light001", 60)
        smart_light.switch_on()
        self.assertEqual(smart_light.switch, "on")

    def test_switch_off(self):
        smart_light = SmartLight("light001", 60)
        smart_light.switch_off()
        self.assertEqual(smart_light.switch, "off")

    def test_get_value(self):
        smart_light = SmartLight("light001", 60)
        self.assertEqual(smart_light.get_value(), 90)

    def test_set_value_within_range(self):
        smart_light = SmartLight("light001", 60)
        smart_light.set_value(75)
        self.assertEqual(smart_light.brightness, 75)

    def test_set_value_above_maximum(self):
        smart_light = SmartLight("light001", 60)
        smart_light.set_value(150)
        self.assertEqual(smart_light.brightness, smart_light.thres_max)

    def test_set_value_below_minimum(self):
        smart_light = SmartLight("light001", 60)
        smart_light.set_value(-10)
        self.assertEqual(smart_light.brightness, smart_light.thres_min)

    def test_get_readings(self):
        smart_light = SmartLight("light001", 60)
        readings = smart_light.get_readings()
        self.assertEqual(readings['identifier'], "light001")
        self.assertEqual(readings['status'], "active")
        self.assertEqual(readings['threshold'], 60)
        self.assertEqual(readings['switch'], "on")
        self.assertEqual(readings['brightness'], 90)

class TestMotionSensor(unittest.TestCase):

    def test_initialization(self):
        motion_sensor = MotionSensor("sensor001", 5)
        self.assertEqual(motion_sensor.identifier, "sensor001")
        self.assertEqual(motion_sensor.status, "active")
        self.assertEqual(motion_sensor.threshold, 5)
        self.assertEqual(motion_sensor.motion, 0)
        self.assertEqual(motion_sensor.switch, "on")

    def test_switch_on(self):
        motion_sensor = MotionSensor("sensor001", 5)
        motion_sensor.switch_on()
        self.assertEqual(motion_sensor.switch, "on")

    def test_switch_off(self):
        motion_sensor = MotionSensor("sensor001", 5)
        motion_sensor.switch_off()
        self.assertEqual(motion_sensor.switch, "off")

    def test_set_value_within_range(self):
        motion_sensor = MotionSensor("sensor001", 5)
        motion_sensor.set_value(7)
        self.assertEqual(motion_sensor.motion, 7)

    def test_set_value_below_minimum(self):
        motion_sensor = MotionSensor("sensor001", 5)
        motion_sensor.set_value(-1)
        self.assertEqual(motion_sensor.motion, motion_sensor.thres_min)

    def test_get_value(self):
        motion_sensor = MotionSensor("sensor001", 5)
        self.assertEqual(motion_sensor.get_value(), 0)

    def test_get_readings(self):
        motion_sensor = MotionSensor("sensor001", 5)
        readings = motion_sensor.get_readings()
        self.assertEqual(readings['identifier'], "sensor001")
        self.assertEqual(readings['status'], "active")
        self.assertEqual(readings['threshold'], 5)
        self.assertEqual(readings['switch'], "on")
        self.assertEqual(readings['motion'], 0)

class TestSmartLock(unittest.TestCase):

    def test_initialization(self):
        smart_lock = SmartLock("lock001")
        self.assertEqual(smart_lock.identifier, "lock001")
        self.assertEqual(smart_lock.status, "active")
        self.assertEqual(smart_lock.switch, "on")

    def test_lock_inactive_device(self):
        smart_lock = SmartLock("lock001")
        smart_lock.status = "inactive"
        smart_lock.lock()
        self.assertEqual(smart_lock.switch, "on")

    def test_lock_active_device(self):
        smart_lock = SmartLock("lock001")
        smart_lock.lock()
        self.assertEqual(smart_lock.switch, "on")

    def test_unlock_inactive_device(self):
        smart_lock = SmartLock("lock001")
        smart_lock.status = "inactive"
        smart_lock.unlock()
        self.assertEqual(smart_lock.switch, "on")

    def test_unlock_active_device(self):
        smart_lock = SmartLock("lock001")
        smart_lock.unlock()
        self.assertEqual(smart_lock.switch, "off")

    def test_get_readings(self):
        smart_lock = SmartLock("lock001")
        readings = smart_lock.get_readings()
        self.assertEqual(readings['identifier'], "lock001")
        self.assertEqual(readings['status'], "active")
        self.assertEqual(readings['switch'], "on")

class TestThermostat(unittest.TestCase):

    def test_initialization(self):
        thermostat = Thermostat("thermo001", 23)
        self.assertEqual(thermostat.identifier, "thermo001")
        self.assertEqual(thermostat.status, "active")
        self.assertEqual(thermostat.threshold, 23)
        self.assertEqual(thermostat.temp, 15.0)
        self.assertEqual(thermostat.switch, "on")

    def test_switch_on(self):
        thermostat = Thermostat("thermo001", 23)
        thermostat.switch_on()
        self.assertEqual(thermostat.switch, "on")

    def test_switch_off(self):
        thermostat = Thermostat("thermo001", 23)
        thermostat.switch_off()
        self.assertEqual(thermostat.switch, "off")

    def test_set_value(self):
        thermostat = Thermostat("thermo001", 23)
        thermostat.set_value(25.5)
        self.assertEqual(thermostat.temp, 25.5)

    def test_get_value(self):
        thermostat = Thermostat("thermo001", 23)
        self.assertEqual(thermostat.get_value(), 15.0)

    def test_get_readings(self):
        thermostat = Thermostat("thermo001", 23)
        readings = thermostat.get_readings()
        self.assertEqual(readings['identifier'], "thermo001")
        self.assertEqual(readings['status'], "active")
        self.assertEqual(readings['threshold'], 23)
        self.assertEqual(readings['switch'], "on")
        self.assertEqual(readings['temp'], 15.0)

if __name__ == '__main__':
    unittest.main()
