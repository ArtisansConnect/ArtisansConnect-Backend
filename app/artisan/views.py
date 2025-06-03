from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import (
    RequestRecrutementSerializer,
    UpdateArtisanProfileSerializer,
    ElectricalTasksArtisanSerializer,
    ElectricalUpdateProgressSerializer
)
from .serializers import (
    ElectricalTasksArtisanSerializer, ElectricalUpdateProgressSerializer,
    PaintingTasksArtisanSerializer, PaintingUpdateProgressSerializer,
    FlooringTasksArtisanSerializer, FlooringUpdateProgressSerializer,
    HvacTasksArtisanSerializer, HvacUpdateProgressSerializer,
    PlumbingTasksArtisanSerializer, PlumbingUpdateProgressSerializer,
    WindowsDoorsTasksArtisanSerializer, WindowsDoorsUpdateProgressSerializer,
    RoofingTasksArtisanSerializer, RoofingUpdateProgressSerializer,
    ConstructionHouseTasksArtisanSerializer, ConstructionHouseUpdateProgressSerializer,
    FacadeTasksArtisanSerializer, FacadeUpdateProgressSerializer
)
from rest_framework.response import Response
from rest_framework import status
from core.permissions import (
    IsArtisan
)
from core.models import (
    CustomUser,
    ElectricalService
)
from core.models import (
    ElectricalService, PaintingService, FlooringService, HvacService,
    PlumbingService, WindowsDoorsService, RoofingService,
    ConstructionHouseService, FacadeService
)
from django.shortcuts import get_object_or_404


# Any user could request a recrutement by filling the informations and waiting for the manager to accept recrutement
class RequestRecrutement(APIView):
    serializer_class = RequestRecrutementSerializer
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = RequestRecrutementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_active=False,role='Artisan')
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# The Artisan can update the informations of his active profile after login    
class UpdateArtisanProfile(APIView):
    serializer_class = UpdateArtisanProfileSerializer
    permission_classes = [IsArtisan]   

    def patch(self,request):
        instance = get_object_or_404(CustomUser,pk=request.user.id)
        serializer = UpdateArtisanProfileSerializer(instance,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

# Each Artisan can see their tasks after authenticate

#Electrical
class ListElectricalTasks(APIView):
    serializer_class =  ElectricalTasksArtisanSerializer
    permission_classes = [IsArtisan]    

    def get(self,request):
        instance = ElectricalService.objects.filter(artisan=request.user)
        serializer = ElectricalTasksArtisanSerializer(instance,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class UpdateElectricalProgress(APIView):
    serializer_class = ElectricalUpdateProgressSerializer  
    permission_classes = [IsArtisan]

    def patch(self,request,pk=None):
        try:
            instance = ElectricalService.objects.get(pk=pk,artisan=request.user)
        except ElectricalService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer =  ElectricalUpdateProgressSerializer(instance,data=request.data,partial=True)   
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    
# Painting
class ListPaintingTasks(APIView):
    serializer_class = PaintingTasksArtisanSerializer
    permission_classes = [IsArtisan]

    def get(self, request):
        instance = PaintingService.objects.filter(artisan=request.user)
        serializer = PaintingTasksArtisanSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdatePaintingProgress(APIView):
    serializer_class = PaintingUpdateProgressSerializer
    permission_classes = [IsArtisan]

    def patch(self, request, pk=None):
        try:
            instance = PaintingService.objects.get(pk=pk, artisan=request.user)
        except PaintingService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PaintingUpdateProgressSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Flooring
class ListFlooringTasks(APIView):
    serializer_class = FlooringTasksArtisanSerializer
    permission_classes = [IsArtisan]

    def get(self, request):
        instance = FlooringService.objects.filter(artisan=request.user)
        serializer = FlooringTasksArtisanSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateFlooringProgress(APIView):
    serializer_class = FlooringUpdateProgressSerializer
    permission_classes = [IsArtisan]

    def patch(self, request, pk=None):
        try:
            instance = FlooringService.objects.get(pk=pk, artisan=request.user)
        except FlooringService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FlooringUpdateProgressSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# HVAC
class ListHvacTasks(APIView):
    serializer_class = HvacTasksArtisanSerializer
    permission_classes = [IsArtisan]

    def get(self, request):
        instance = HvacService.objects.filter(artisan=request.user)
        serializer = HvacTasksArtisanSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateHvacProgress(APIView):
    serializer_class = HvacUpdateProgressSerializer
    permission_classes = [IsArtisan]

    def patch(self, request, pk=None):
        try:
            instance = HvacService.objects.get(pk=pk, artisan=request.user)
        except HvacService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = HvacUpdateProgressSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Plumbing
class ListPlumbingTasks(APIView):
    serializer_class = PlumbingTasksArtisanSerializer
    permission_classes = [IsArtisan]

    def get(self, request):
        instance = PlumbingService.objects.filter(artisan=request.user)
        serializer = PlumbingTasksArtisanSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdatePlumbingProgress(APIView):
    serializer_class = PlumbingUpdateProgressSerializer
    permission_classes = [IsArtisan]

    def patch(self, request, pk=None):
        try:
            instance = PlumbingService.objects.get(pk=pk, artisan=request.user)
        except PlumbingService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PlumbingUpdateProgressSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Windows & Doors
class ListWindowsDoorsTasks(APIView):
    serializer_class = WindowsDoorsTasksArtisanSerializer
    permission_classes = [IsArtisan]

    def get(self, request):
        instance = WindowsDoorsService.objects.filter(artisan=request.user)
        serializer = WindowsDoorsTasksArtisanSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateWindowsDoorsProgress(APIView):
    serializer_class = WindowsDoorsUpdateProgressSerializer
    permission_classes = [IsArtisan]

    def patch(self, request, pk=None):
        try:
            instance = WindowsDoorsService.objects.get(pk=pk, artisan=request.user)
        except WindowsDoorsService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WindowsDoorsUpdateProgressSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Roofing
class ListRoofingTasks(APIView):
    serializer_class = RoofingTasksArtisanSerializer
    permission_classes = [IsArtisan]

    def get(self, request):
        instance = RoofingService.objects.filter(artisan=request.user)
        serializer = RoofingTasksArtisanSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateRoofingProgress(APIView):
    serializer_class = RoofingUpdateProgressSerializer
    permission_classes = [IsArtisan]

    def patch(self, request, pk=None):
        try:
            instance = RoofingService.objects.get(pk=pk, artisan=request.user)
        except RoofingService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RoofingUpdateProgressSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Construction House
class ListConstructionHouseTasks(APIView):
    serializer_class = ConstructionHouseTasksArtisanSerializer
    permission_classes = [IsArtisan]

    def get(self, request):
        instance = ConstructionHouseService.objects.filter(artisan=request.user)
        serializer = ConstructionHouseTasksArtisanSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateConstructionHouseProgress(APIView):
    serializer_class = ConstructionHouseUpdateProgressSerializer
    permission_classes = [IsArtisan]

    def patch(self, request, pk=None):
        try:
            instance = ConstructionHouseService.objects.get(pk=pk, artisan=request.user)
        except ConstructionHouseService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ConstructionHouseUpdateProgressSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Facade
class ListFacadeTasks(APIView):
    serializer_class = FacadeTasksArtisanSerializer
    permission_classes = [IsArtisan]

    def get(self, request):
        instance = FacadeService.objects.filter(artisan=request.user)
        serializer = FacadeTasksArtisanSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateFacadeProgress(APIView):
    serializer_class = FacadeUpdateProgressSerializer
    permission_classes = [IsArtisan]

    def patch(self, request, pk=None):
        try:
            instance = FacadeService.objects.get(pk=pk, artisan=request.user)
        except FacadeService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FacadeUpdateProgressSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
