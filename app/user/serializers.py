from rest_framework.serializers import ModelSerializer
from core.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['role'] = user.role if hasattr(user, 'role') else 'user'
        token['email'] = user.email
        token['firstName'] = user.firstName
        token['lastName'] = user.lastName
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add extra fields to response
        data['role'] = self.user.role if hasattr(self.user, 'role') else 'user'
        data['email'] = self.user.email
        data['firstName'] = self.user.firstName
        data['lastName'] = self.user.lastName
        return data

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','firstName','lastName','phoneNumber','password','role']
        extra_kwargs = {'password':{'write_only':True}, 
                        'role':{'read_only':True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user  

class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','firstName','lastName','image']   
        extra_fields = {
            'password' : {'write_only':True, 'required':False}
        }   

        def update(self, instance,validated_data):
            password = validated_data.pop('password', None)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            if password:
                instance.set_password(password)

            instance.save()
            return instance
        

class ProfileUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','firstName','lastName','image'] 

class ProfilesUsersSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','firstName','lastName']  