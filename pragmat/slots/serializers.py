from rest_framework import serializers
from .models import Slot

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = [
            'id', 'name', 'game_symbol', 'logo', 'description', 'snippet', 'slug',
            'rtp', 'rating', 'users_choice', 'sorting_order', 'is_new', 'is_popular'
        ]
