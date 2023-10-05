from rest_framework import serializers
from base.models import Item,Nota
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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