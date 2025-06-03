from .models import *

def is_artisan_available(artisan, start_dt, end_dt):
    all_services = [
        ElectricalService, PlumbingService, PaintingService, FlooringService,
        ConstructionHouseService, RoofingService, FacadeService, WindowsDoorsService, HvacService
    ]

    for service_model in all_services:
        conflicts = service_model.objects.filter(
            artisan=artisan,
            start_date__lt=end_dt,
            end_date__gt=start_dt
        )
        if conflicts.exists():
            return False
    return True


def find_available_artisan(service_type, start_dt, end_dt):
    artisans = CustomUser.objects.filter(role='Artisan', roleArtisan=service_type)
    for artisan in artisans:
        if is_artisan_available(artisan, start_dt, end_dt):
            return artisan
    return None
