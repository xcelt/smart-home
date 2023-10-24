from models import Sensor

camera = Sensor(name="camera")
thermostat = Sensor(name="thermostat")
lighting = Sensor(name="lighting")
smart_lock = Sensor(name="smart_lock")

Sensor.display_sensors(True)

# for sensor in Sensor:
#     print(sensor, sensor.value)
# sensors =["camera", "thermostat", "lighting", "smart-lock"]


# for sensor in sensors:
#      if sensor == "active":
#          print(f"{sensor.id} is connected")
#      else:
#          print("No devices found")
