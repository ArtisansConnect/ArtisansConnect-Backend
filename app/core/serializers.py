# serializers.py
from rest_framework import serializers
from .models import ElectricalService,PaintingService,FlooringService,HvacService

class ElectricalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricalService
        fields = '__all__'
        read_only_fields = ['cost', 'cableLength']


class PaintingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaintingService
        fields = '__all__'
        read_only_fields = ['cost']  

class FlooringServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlooringService
        fields = '__all__'
        read_only_fields = ['cost']   

class HvacServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HvacService
        fields = ['id', 'user', 'smallHvac', 'mediumHvac', 'bigHvac', 'cost']
        read_only_fields = ['cost']  