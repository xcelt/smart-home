# from django.db import models
# import json
# import random



class Sensor:

    sensorList = []

    def __init__(self, name: str): #threshold=50):
        self.name = name 
        Sensor.activate_sensor(self)     # active or inactive
        # threshold = self.setThreshold(threshold)
        Sensor.sensorList.append(self)

    def activate_sensor(self):
        self.active = True
    
    def deactivate_sensor(self):
        self.active = False

    def get_status(self):
        return self.active

    def display_sensors(active: bool = True):
        
        if Sensor.sensorList:
            print("No devices found")
        else:
            for sensor in Sensor.sensorList:
                if sensor.get_status == active:
                    print(f"{sensor.id} is connected")
            

    # def setThreshold(self, threshold, value,):
    #     if value > self.THRES_MAX:
    #         threshold = self.THRES_MAX
    #     elif value < self.THRES_MIN:
    #         threshold = self.THRES_MIN
    #     else:
    #         threshold = value
    
    # def sensorLocate(self, id, status, threshold):
    #     return{'id':id, 'status':status, 'threshold':threshold}

    def __str__(self) -> str:
        return self.name
    