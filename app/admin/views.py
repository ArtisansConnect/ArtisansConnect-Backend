from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from .serializers import UserListSerializer
from core.permissions import IsAdmin
from core.models import CustomUser

class UserListView(ListCreateAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAdmin]
    queryset = CustomUser.objects.all()


class UserEditView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAdmin]
    queryset = CustomUser.objects.all()