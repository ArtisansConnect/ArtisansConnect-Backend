from django.contrib import admin
from .models import CustomUser,ElectricalService,PaintingService,FlooringService,HvacService

admin.site.register(CustomUser)
admin.site.register(ElectricalService)
admin.site.register(PaintingService)
admin.site.register(FlooringService)
admin.site.register(HvacService)