from django.contrib import admin
from .models import CustomUser,ElectricalService,PaintingService,FlooringService

admin.site.register(CustomUser)
admin.site.register(ElectricalService)
admin.site.register(PaintingService)
admin.site.register(FlooringService)