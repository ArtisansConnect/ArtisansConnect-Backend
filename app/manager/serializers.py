from core.models import *
from rest_framework.serializers import ModelSerializer

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'       
        read_only_fields = ['user','date']

# The Manager can Accept the recrutement of an inactive artisan
class AcceptRecrutementSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['is_active']   

# The Manager could see the list of artisans
class ListArtisanSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
<<<<<<< HEAD
        fields = ['id','email','phoneNumber','firstName','lastName','roleArtisan','location','is_active','date_joined','diplomDocument']
=======
        fields = ['id','email','phoneNumber','firstName','lastName','roleArtisan','location','is_active','date_joined','diplomDocument']




# Affect Artisan to a Service logic

# Project Serializers  
                             
from rest_framework import serializers
from core.models import (
    Project,
    ElectricalService, PaintingService, PlumbingService, FlooringService,
    HvacService, WindowsDoorsService, RoofingService, ConstructionHouseService,
    FacadeService, CustomUser
)
from django.db.models import Q

class BaseServiceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['artisan']

class ElectricalProjectSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = ElectricalService

class PaintingProjectSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = PaintingService

class PlumbingProjectSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = PlumbingService

class FlooringProjectSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = FlooringService

class HvacProjectSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = HvacService

class CarpentaryProjectSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = WindowsDoorsService

class RoofingProjectSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = RoofingService

class ConstructionProjectSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = ConstructionHouseService

class FacadeProjectSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = FacadeService


class AffectServiceArtisanSerializer(serializers.ModelSerializer):
    electrical = ElectricalProjectSerializer(required=False)
    painting = PaintingProjectSerializer(required=False)
    hvac = HvacProjectSerializer(required=False)
    flooring = FlooringProjectSerializer(required=False)
    plumbing = PlumbingProjectSerializer(required=False)
    carpentary = CarpentaryProjectSerializer(required=False)
    roofing = RoofingProjectSerializer(required=False)
    construction = ConstructionProjectSerializer(required=False)
    facade = FacadeProjectSerializer(required=False)

    class Meta:
        model = Project
        fields = [
            'id', 'electrical', 'painting', 'hvac', 'flooring',
            'plumbing', 'carpentary', 'roofing', 'construction', 'facade'
        ]

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user if request else None

        if not user or user.role != 'Manager':
            raise serializers.ValidationError("Only managers can assign artisans.")

        service_map = {
            'electrical': ('electrical', 'Electricity', ElectricalService),
            'painting': ('painting', 'Painting', PaintingService),
            'hvac': ('hvac', 'Hvac', HvacService),
            'flooring': ('flooring', 'Flooring', FlooringService),
            'plumbing': ('plumbing', 'Plumbing', PlumbingService),
            'carpentary': ('carpentary', 'Carpentary', WindowsDoorsService),
            'roofing': ('roofing', 'Roofing', RoofingService),
            'construction': ('construction', 'Construction', ConstructionHouseService),
            'facade': ('facade', 'Facade', FacadeService),
        }

        for field_name, (project_field, expected_role, model_class) in service_map.items():
            service_data = validated_data.get(field_name)
            if service_data:
                service_instance = getattr(instance, project_field)
                if service_instance:
                    artisan = service_data.get('artisan')
                    if artisan.role != 'Artisan' or artisan.roleArtisan != expected_role:
                        raise serializers.ValidationError(
                            f"Artisan for '{field_name}' must have role '{expected_role}'"
                        )
                    # Check if artisan is available
                    if not self.is_artisan_available(artisan, service_instance, model_class):
                        raise serializers.ValidationError(
                            f"Artisan '{artisan.email}' is already assigned to another project during the same time."
                        )
                    service_instance.artisan = artisan
                    service_instance.save()
        return instance

    def is_artisan_available(self, artisan, current_service, model_class):
        # Check for overlapping date assignments with the same artisan
        return not model_class.objects.filter(
            artisan=artisan,
            start_date__lt=current_service.end_date,
            end_date__gt=current_service.start_date
        ).exclude(id=current_service.id).exists()
>>>>>>> a23c7b6687d8d8c0c828b693c6210eeeb56a21dc
