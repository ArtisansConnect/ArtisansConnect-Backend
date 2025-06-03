from core.models import Tags,Blog,CustomUser
from rest_framework.serializers import ModelSerializer

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'       
        read_only_fields = ['user','date']

# The Manager can Accept the recrutement of an inactive artisan
class AcceptRecrutementSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['is_active']   

# The Manager could see the list of artisans
class ListArtisanSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','phoneNumber','firstName','lastName','roleArtisan','location','is_active','date_joined','diplomDocument']