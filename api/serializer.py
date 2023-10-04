from rest_framework import serializers
from base.models import Item,Nota

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= Item
        fields='__all__'
class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model= Nota
        fields='__all__'