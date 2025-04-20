# serializers.py
from rest_framework import serializers
from .models import ElectricalService

class ElectricalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricalService
        fields = '__all__'
        read_only_fields = ['cost', 'cableLength']