# serializers.py
from rest_framework import serializers
from .models import Sites, Casino, Bonus, Content

class SitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sites
        fields = '__all__'

class CasinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Casino
        fields = '__all__'

class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonus
        fields = '__all__'

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
