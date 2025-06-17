from rest_framework.serializers import ModelSerializer
from core.models import CustomUser, Project

class UserListSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ProjectAdminSerialzier(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'