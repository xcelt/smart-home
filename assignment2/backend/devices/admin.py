from django.contrib import admin
from .models import Devices

class DevicesAdmin(admin.ModelAdmin):
    list_display = ("name", "activated", "enabled")

admin.site.register(Devices, DevicesAdmin)