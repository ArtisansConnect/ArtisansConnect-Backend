from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import (
    RequestRecrutementSerializer,
    UpdateArtisanProfileSerializer,
    ElectricalTasksArtisan
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
class ListElectricalTasks(APIView):
    serializer_class =  ElectricalTasksArtisan
    permission_classes = [IsArtisan]    

    def get(self,request):
        instance = ElectricalService.objects.filter(artisan=request.user)
        serializer = ElectricalTasksArtisan(instance,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class UpdateElectricalProgress(APIView):
    serializer_class = ElectricalService  