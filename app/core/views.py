# views.py
from rest_framework import viewsets
from .models import ElectricalService,PaintingService
from .serializers import ElectricalServiceSerializer,PaintingServiceSerializer

class ElectricalServiceViewSet(viewsets.ModelViewSet):
    queryset = ElectricalService.objects.all()
    serializer_class = ElectricalServiceSerializer

class PaintingServiceViewSet(viewsets.ModelViewSet):
    queryset = PaintingService.objects.all()
    serializer_class = PaintingServiceSerializer