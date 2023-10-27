from django.db import models

class Temperature(models.Model):
    DEFAULT_TEMPERATURE = 22
    currentTemperature = DEFAULT_TEMPERATURE
    
    currentTemperature = models.IntegerField(max_length=2)
    
  #  def increase_temperature(self):
  #      self.currentTemperature += 1
        
  #  def decrease_temperature(self):
  #      self.currentTemperature -= 1 

    def __str__(self):
        return self.currentTemperature