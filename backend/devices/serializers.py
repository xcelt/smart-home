from rest_framework import serializers
from .models import Devices

# Serializers change the model into JSON
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices
        fields = ('id', 'name', 'activated', 'enabled') # 'fields' must have 's'