from rest_framework import serializers
from base.models import Item,Nota,CustomUser,Post,MyModel
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'name', 'post_id', 'image')
class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'

CustomUser = get_user_model()
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= Item
        fields='__all__'
class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model= Nota
        fields='__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        # Add any other user data you want to include in the response
        return data
    # auth/serializers.py


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password','id_tipousuario')  # Add other fields as needed
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            id_tipousuario=validated_data['id_tipousuario']
        )
        return user
    
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)