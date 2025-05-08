# serializers.py
from rest_framework import serializers
from .models import (ElectricalService,
                     PaintingService,
                     FlooringService,
                     HvacService,
                     PlumbingService,
                     WindowsDoorsService,
                     RoofingService,
                     ConstructionHouseService,
                     FacadeService)

class ElectricalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricalService
        fields = '__all__'
        read_only_fields = ['user','cost', 'cableLength']


class PaintingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaintingService
        fields = '__all__'
        read_only_fields = ['user','cost']  

class FlooringServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlooringService
        fields = '__all__'
        read_only_fields = ['user','cost']   

class HvacServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HvacService
        fields = ['id','user', 'smallHvac', 'mediumHvac', 'bigHvac', 'cost']
        read_only_fields = ['user','cost']  

class PlumbingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlumbingService
        fields = '__all__'
        read_only_fields = ['user','cost','time']      

class WindowsDoorsServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindowsDoorsService
        fields = '__all__'
        read_only_fields = ['user','time','cost']                

class RoofingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoofingService
        fields = '__all__'
        read_only_fields = ['user','time','cost'] 

class ConstructionHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionHouseService
        fields = '__all__'
        read_only_fields = ['user','time','cost'] 

class FacadeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacadeService
        fields = '__all__'
        read_only_fields = ['user','time','cost']                            