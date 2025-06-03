from rest_framework.serializers import ModelSerializer
from core.models import (
    ElectricalService, PaintingService, FlooringService, HvacService,
    PlumbingService, WindowsDoorsService, RoofingService,
    ConstructionHouseService, FacadeService,CustomUser
)

class RequestRecrutementSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','firstName','lastName',
                  'phoneNumber','location','roleArtisan',
                  'diplomDocument','password']               
        read_only_fields = ['id','role','is_active','date_joined']
        write_only_fields = ['password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user  
        
class UpdateArtisanProfileSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','firstName','lastName',
                  'phoneNumber','image','location']       


# Update Progress and See tasks by Artisan
# Electrical
class ElectricalTasksArtisanSerializer(ModelSerializer):  
    class Meta:
        model = ElectricalService
        fields = ['id','artisan','start_date','end_date','time'] 

class ElectricalUpdateProgressSerializer(ModelSerializer):
    class Meta:
        model = ElectricalService
        fields = ['progress']


# Painting
class PaintingTasksArtisanSerializer(ModelSerializer):  
    class Meta:
        model = PaintingService
        fields = ['id','artisan','start_date','end_date','time'] 

class PaintingUpdateProgressSerializer(ModelSerializer):
    class Meta:
        model = PaintingService
        fields = ['progress']


# Flooring
class FlooringTasksArtisanSerializer(ModelSerializer):  
    class Meta:
        model = FlooringService
        fields = ['id','artisan','start_date','end_date','time'] 

class FlooringUpdateProgressSerializer(ModelSerializer):
    class Meta:
        model = FlooringService
        fields = ['progress']


# HVAC
class HvacTasksArtisanSerializer(ModelSerializer):  
    class Meta:
        model = HvacService
        fields = ['id','artisan','start_date','end_date','time'] 

class HvacUpdateProgressSerializer(ModelSerializer):
    class Meta:
        model = HvacService
        fields = ['progress']


# Plumbing
class PlumbingTasksArtisanSerializer(ModelSerializer):  
    class Meta:
        model = PlumbingService
        fields = ['id','artisan','start_date','end_date','time'] 

class PlumbingUpdateProgressSerializer(ModelSerializer):
    class Meta:
        model = PlumbingService
        fields = ['progress']


# Windows & Doors
class WindowsDoorsTasksArtisanSerializer(ModelSerializer):  
    class Meta:
        model = WindowsDoorsService
        fields = ['id','artisan','start_date','end_date','time'] 

class WindowsDoorsUpdateProgressSerializer(ModelSerializer):
    class Meta:
        model = WindowsDoorsService
        fields = ['progress']


# Roofing
class RoofingTasksArtisanSerializer(ModelSerializer):  
    class Meta:
        model = RoofingService
        fields = ['id','artisan','start_date','end_date','time'] 

class RoofingUpdateProgressSerializer(ModelSerializer):
    class Meta:
        model = RoofingService
        fields = ['progress']


# Construction House
class ConstructionHouseTasksArtisanSerializer(ModelSerializer):  
    class Meta:
        model = ConstructionHouseService
        fields = ['id','artisan','start_date','end_date','time'] 

class ConstructionHouseUpdateProgressSerializer(ModelSerializer):
    class Meta:
        model = ConstructionHouseService
        fields = ['progress']


# Facade
class FacadeTasksArtisanSerializer(ModelSerializer):  
    class Meta:
        model = FacadeService
        fields = ['id','artisan','start_date','end_date','time'] 

class FacadeUpdateProgressSerializer(ModelSerializer):
    class Meta:
        model = FacadeService
        fields = ['progress']   