from rest_framework import serializers
from .models import  *


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ProductSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'photo', 'category']

    def get_photo(self, obj):
        request = self.context.get('request')
        photo_url = obj.photo.url
        return request.build_absolute_uri(photo_url)



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'