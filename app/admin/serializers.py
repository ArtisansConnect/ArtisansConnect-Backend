from rest_framework.serializers import ModelSerializer
from core.models import CustomUser

class UserListSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'