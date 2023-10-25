from django.shortcuts import render
from rest_framework import viewsets
from .serializers import DeviceSerializer
from .models import Devices

class DevicesView(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer
    queryset = Devices.objects.all()