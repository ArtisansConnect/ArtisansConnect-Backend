# serializers.py
from rest_framework import serializers
from .models import ElectricalService,PaintingService

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