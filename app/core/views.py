# views.py
from rest_framework import viewsets
from .models import ElectricalService
from .serializers import ElectricalServiceSerializer

class ElectricalServiceViewSet(viewsets.ModelViewSet):
    queryset = ElectricalService.objects.all()
    serializer_class = ElectricalServiceSerializer
