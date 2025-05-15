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
                     Project,
                     Planification)

class ElectricalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricalService
        fields = '__all__'
        read_only_fields = ['user','cost', 'cableLength','time']


class PaintingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaintingService
        fields = '__all__'
        read_only_fields = ['user','cost','time']  

class FlooringServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlooringService
        fields = '__all__'
        read_only_fields = ['user','cost','time']   

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
        fields = ['id','time','cost','start_date','end_date','rank']


class PaintingProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaintingService
        fields = ['id','time','cost','start_date','end_date','rank']

class HvacProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = HvacService
        fields = ['id','time','cost','start_date','end_date','rank']        

class FlooringProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlooringService
        fields = ['id','time','cost','start_date','end_date','rank']         

class PlumbingProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaintingService
        fields = ['id','time','cost','start_date','end_date','rank']

class CarpentaryProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindowsDoorsService
        fields = ['id','time','cost','start_date','end_date','rank']

class RoofingProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoofingService
        fields = ['id','time','cost','start_date','end_date','rank']


class ConstructionProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionHouseService
        fields = ['id','time','cost','start_date','end_date','rank']        

class FacadeProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacadeService
        fields = ['id','time','cost','start_date','end_date','rank']           


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

    def get_total_time(self, obj):
        # Helper to safely get time or return 0 if None
        def safe_time(service):
            return getattr(service, 'time', 0) or 0

        construction_time = safe_time(obj.construction)
        group1 = max(
            safe_time(obj.electrical),
            safe_time(obj.plumbing),
            safe_time(obj.hvac)
        )
        painting_time = safe_time(obj.painting)
        flooring_time = safe_time(obj.flooring)
        group2 = max(
            safe_time(obj.carpentary),
            safe_time(obj.facade),
            safe_time(obj.roofing)
        )

        total = round(
            construction_time + group1 + painting_time + flooring_time + group2,
            0
        )
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



# Planification Serializer
class ProjectPlanificationSerializer(serializers.ModelSerializer):
    electrical = ElectricalProjectSerializer(read_only=True)
    painting = PaintingProjectSerializer(read_only=True)
    hvac = HvacProjectSerializer(read_only=True)
    flooring = FlooringProjectSerializer(read_only=True)
    plumbing = PlumbingProjectSerializer(read_only=True)
    carpentary = CarpentaryProjectSerializer(read_only=True)
    roofing = RoofingProjectSerializer(read_only=True)
    construction = ConstructionProjectSerializer(read_only=True)
    facade = FacadeProjectSerializer(read_only=True)
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['user','status']       


class PlanificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planification
        fields = '__all__'     
        
class PlanificationListSerializer(serializers.ModelSerializer):
    project = ProjectPlanificationSerializer(read_only=True)
    class Meta:
        model = Planification
        fields = '__all__'  


# The manager can refuse the project request
class UpdateProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = 'status'      
                                        