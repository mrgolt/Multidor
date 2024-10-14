from rest_framework import serializers
from .models import Slot, SlotDescription, Theme, Paylines, Feature

class SlotSerializer(serializers.ModelSerializer):
    theme = serializers.CharField(write_only=True, required=False)
    features = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    paylines = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Slot
        fields = '__all__'

    def create(self, validated_data):
        theme_title = validated_data.pop('theme', None)
        features_list = validated_data.pop('features', [])
        paylines_title = validated_data.pop('paylines', None)

        # Найти объекты Theme, Feature и Paylines по переданным строкам
        theme_instance = Theme.objects.filter(title=theme_title).first()
        paylines_instance = Paylines.objects.filter(title=paylines_title).first()
        feature_instances = Feature.objects.filter(title__in=features_list)

        # Создать объект Slot
        slot = Slot.objects.create(
            **validated_data,  # Все остальные данные передаются как есть
            theme=theme_instance,
            paylines=paylines_instance
        )

        # Добавить ManyToMany поле для Features
        slot.features.set(feature_instances)
        slot.save()

        return slot


class SlotDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotDescription
        fields = ['id', 'site', 'slot', 'description', 'snippet']  # Укажите поля, которые хотите включить в сериализатор

