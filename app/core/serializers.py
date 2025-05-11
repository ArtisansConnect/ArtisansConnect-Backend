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
                     FacadeService,
                     Project)

class ElectricalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricalService
        fields = '__all__'
        read_only_fields = ['user','cost', 'cableLength']


class PaintingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaintingService
        fields = '__all__'
        read_only_fields = ['user','cost','time']  

class FlooringServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlooringService
        fields = '__all__'
        read_only_fields = ['user','cost']   

class HvacServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HvacService
        fields = '__all__'
        read_only_fields = ['user','cost','time']  

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




# Project Serializers  
                             
class ElectricalProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricalService
        fields = ['id','time','cost']


class PaintingProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaintingService
        fields = ['id','time','cost']

class HvacProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = HvacService
        fields = ['id','time','cost']        

class FlooringProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlooringService
        fields = ['id','user','cost']         

class PlumbingProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaintingService
        fields = ['id','time','cost']

class CarpentaryProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindowsDoorsService
        fields = ['id','time','cost']

class RoofingProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoofingService
        fields = ['id','time','cost']

class ConstructionProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionHouseService
        fields = ['id','time','cost']        

class FacadeProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacadeService
        fields = ['id','time','cost']           


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['user','start_date','status']          


class ProjectListSerializer(serializers.ModelSerializer):
    electrical = ElectricalProjectSerializer(read_only=True)
    painting = PaintingProjectSerializer(read_only=True)
    hvac = HvacProjectSerializer(read_only=True)
    flooring = FlooringProjectSerializer(read_only=True)
    plumbing = PlumbingProjectSerializer(read_only=True)
    carpentary = CarpentaryProjectSerializer(read_only=True)
    roofing = RoofingProjectSerializer(read_only=True)
    construction = ConstructionProjectSerializer(read_only=True)
    facade = FacadeProjectSerializer(read_only=True)
    total_time = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['user','start_date','status']                   

    def get_total_time(self,obj):
        time_fields = [
            getattr(obj.electrical, 'time',0), 
            getattr(obj.painting, 'time', 0),
            getattr(obj.hvac, 'time', 0),
            getattr(obj.plumbing, 'time', 0),
            getattr(obj.flooring, 'time', 0),
            getattr(obj.carpentary, 'time', 0),
            getattr(obj.roofing, 'time', 0),
            getattr(obj.construction, 'time', 0),
            getattr(obj.facade, 'time', 0),
        ]
        total = round(sum([t for t in time_fields if t is not None]),0)
        return total
    
    def get_total_cost(self, obj):
        cost_fields = [
            getattr(obj.electrical, 'cost', 0),
            getattr(obj.painting, 'cost', 0),
            getattr(obj.hvac, 'cost', 0),
            getattr(obj.plumbing, 'cost', 0),
            getattr(obj.flooring, 'cost', 0),
            getattr(obj.carpentary, 'cost', 0),
            getattr(obj.roofing, 'cost', 0),
            getattr(obj.construction, 'cost', 0),
            getattr(obj.facade, 'cost', 0),
        ]
        total = round(sum([c for c in cost_fields if c is not None]),0)
        return total