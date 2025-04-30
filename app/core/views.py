# views.py
from rest_framework import viewsets,permissions
from .models import (ElectricalService,
                     PaintingService,
                     FlooringService,
                     HvacService,
                     PlumbingService,
                     WindowsDoorsService)
from .serializers import (ElectricalServiceSerializer,
                          PaintingServiceSerializer,
                          FlooringServiceSerializer,
                          HvacServiceSerializer,
                          PlumbingServiceSerializer,
                          WindowsDoorsServiceSerializer)

class ElectricalServiceViewSet(viewsets.ModelViewSet):
    queryset = ElectricalService.objects.all()
    serializer_class = ElectricalServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PaintingServiceViewSet(viewsets.ModelViewSet):
    queryset = PaintingService.objects.all()
    serializer_class = PaintingServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FlooringServiceViewSet(viewsets.ModelViewSet):
    queryset = FlooringService.objects.all()    
    serializer_class = FlooringServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HvacServiceViewSet(viewsets.ModelViewSet):
    queryset = HvacService.objects.all()
    serializer_class = HvacServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  

class PlumbingServiceViewSet(viewsets.ModelViewSet):
    queryset = PlumbingService.objects.all()
    serializer_class = PlumbingServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)          


class WindowsDoorsServiceViewSet(viewsets.ModelViewSet):
    queryset = WindowsDoorsService.objects.all()
    serializer_class = WindowsDoorsServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)                    