from rest_framework import serializers
from .models import Slot, SlotDescription

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = [
            'id', 'name', 'provider'
        ]

class SlotDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotDescription
        fields = ['id', 'site', 'slot', 'description', 'snippet']  # Укажите поля, которые хотите включить в сериализатор

