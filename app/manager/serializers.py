from core.models import Tags,Blog
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