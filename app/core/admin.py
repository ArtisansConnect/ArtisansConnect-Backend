from django.contrib import admin
from django.utils.html import format_html
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
                     Planification,
                     Message,
                     Tags,
                     Blog)

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
admin.site.register(Message)
admin.site.register(Tags)
admin.site.register(Blog)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'firstName', 'lastName', 'role', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:50%;"/>'.format(obj.image.url))
        return "-"
    image_tag.short_description = 'Profile Image'

admin.site.register(CustomUser, CustomUserAdmin)    