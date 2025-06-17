from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from .serializers import UserListSerializer,ProjectAdminSerialzier
from core.permissions import IsAdmin
from core.models import CustomUser,Project

class UserListView(ListCreateAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAdmin]
    queryset = CustomUser.objects.all()


class UserEditView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAdmin]
    queryset = CustomUser.objects.all()


class ProjectViewAdmin(APIView):
    serializer_class = ProjectAdminSerialzier
    permission_classes = [IsAdmin]

    def get(self,request):
        instance = Project.objects.all()
        serializer = ProjectAdminSerialzier(instance,many=True)
        return Response(serializer.data,status = status.HTTP_200_OK)