from django.contrib import admin
from .models import (CustomUser,
                     ElectricalService,
                     PaintingService,
                     FlooringService,
                     HvacService,
                     PlumbingService,
                     FacadeService,
                     ConstructionHouseService,
                     RoofingService,
                     WindowsDoorsService,
                     Project,
                     Planification)

admin.site.register(CustomUser)
admin.site.register(ElectricalService)
admin.site.register(PaintingService)
admin.site.register(FlooringService)
admin.site.register(HvacService)
admin.site.register(PlumbingService)
admin.site.register(FacadeService)
admin.site.register(ConstructionHouseService)
admin.site.register(RoofingService)
admin.site.register(WindowsDoorsService)
admin.site.register(Project)
admin.site.register(Planification)