from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from core.models import CustomUser
from .serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    UpdateUserSerializer,
    ProfileUserSerializer
    )
from rest_framework_simplejwt.views import TokenObtainPairView

class Signup(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UpdateProfile(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class ViewProfile(generics.RetrieveAPIView):  
    serializer_class = ProfileUserSerializer
    permission_classes = [IsAuthenticated]  

    def get_object(self):
        return self.request.user