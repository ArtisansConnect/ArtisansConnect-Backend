from rest_framework.serializers import ModelSerializer
from core.models import CustomUser

class RequestRecrutementSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','firstName','lastName',
                  'phoneNumber','location','roleArtisan',
                  'diplomDocument']               
        read_only_fields = ['role','is_active','date_joined']
        write_only_fields = ['password']

        def create(self, validated_data):
            password = validated_data.pop('password')
            user = CustomUser(**validated_data)
            user.set_password(password)
            user.save()
            return user  
        
class UpdateArtisanProfileSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','firstName','lastName',
                  'phoneNumber','image','location']        