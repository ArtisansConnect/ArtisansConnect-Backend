# views.py
from rest_framework import viewsets
from .models import ElectricalService,PaintingService,FlooringService
from .serializers import ElectricalServiceSerializer,PaintingServiceSerializer,FlooringServiceSerializer

class ElectricalServiceViewSet(viewsets.ModelViewSet):
    queryset = ElectricalService.objects.all()
    serializer_class = ElectricalServiceSerializer

class PaintingServiceViewSet(viewsets.ModelViewSet):
    queryset = PaintingService.objects.all()
    serializer_class = PaintingServiceSerializer

class FlooringServiceViewSet(viewsets.ModelViewSet):
    queryset = FlooringService.objects.all()    
    serializer_class = FlooringServiceSerializer