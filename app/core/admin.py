from django.contrib import admin
from .models import CustomUser,ElectricalService

admin.site.register(CustomUser)
admin.site.register(ElectricalService)