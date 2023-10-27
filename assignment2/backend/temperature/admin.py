from django.contrib import admin
from .models import Temperature

class TemperatureAdmin(admin.ModelAdmin):
    list_display = ()

admin.site.register(Temperature, TemperatureAdmin)