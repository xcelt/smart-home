from rest_framework import serializers
from .models import Temperature

# Serializers change the model into JSON
class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = ('currentTemperature', ) # 'fields' must have 's'