from rest_framework import serializers
from .models import Slot, SlotDescription, Theme, Paylines, Feature

class SlotSerializer(serializers.ModelSerializer):
    theme = serializers.CharField(write_only=True, required=False)
    features = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    paylines = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Slot
        fields = '__all__'
        #fields = ['id', 'provider', 'slot_type', 'theme', 'features', 'paylines']

    def create(self, validated_data):
        theme_title = validated_data.pop('theme', None)
        features_list = validated_data.pop('features', [])
        paylines_title = validated_data.pop('paylines', None)

        # Проверка наличия theme_title и поиск объекта, если передано значение
        if theme_title:
            theme_instance = Theme.objects.filter(title_ru=theme_title).first()
            if theme_instance:
                validated_data['theme'] = theme_instance

        # Проверка наличия paylines_title и поиск объекта, если передано значение
        if paylines_title:
            paylines_instance = Paylines.objects.filter(title_ru=paylines_title).first()
            if paylines_instance:
                validated_data['paylines'] = paylines_instance

        # Проверка наличия features_list и поиск объектов, если передано значение
        if features_list:
            feature_instances = Feature.objects.filter(title_ru__in=features_list)
            validated_data['features'] = feature_instances

        # Создание объекта Slot с проверенными данными
        slot = Slot.objects.create(**validated_data)

        # Добавить ManyToMany поле для Features
        slot.features.set(feature_instances)
        slot.save()

        return slot


class SlotDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotDescription
        fields = '__all__'
        # fields = ['id', 'site', 'slot', 'description', 'snippet', 'language']  # Укажите поля, которые хотите включить в сериализатор

