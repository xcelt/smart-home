from rest_framework import viewsets
from .serializers import TemperatureSerializer
from .models import Temperature

class TemperatureView(viewsets.ModelViewSet):
    serializer_class = TemperatureSerializer
    queryset = Temperature.objects.all()