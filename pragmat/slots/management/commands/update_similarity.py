# slots/management/commands/update_similarity.py
from django.core.management.base import BaseCommand
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from slots.models import Slot
import numpy as np
from collections import defaultdict


class Command(BaseCommand):
    help = 'Обновление косинусного сходства для похожих слотов'

    def handle(self, *args, **kwargs):
        # Группируем слоты по провайдеру
        provider_slots = defaultdict(list)
        for slot in Slot.objects.filter(provider_id=1):
            provider_slots[slot.provider].append(slot)

        # Обновляем похожие слоты для каждого провайдера
        for provider, slots in provider_slots.items():
            texts = [f"{slot.name} {slot.description}" for slot in slots]

            # Векторизация текста
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(texts)

            # Вычисление косинусного сходства
            cosine_similarities = cosine_similarity(tfidf_matrix)

            # Обновление похожих слотов
            for idx, slot in enumerate(slots):
                similar_indices = cosine_similarities[idx].argsort()[-11:-1][::-1]
                similar_slots_ids = [slots[i].id for i in similar_indices]
                slot.similar_slots = similar_slots_ids
                slot.save()

        self.stdout.write(self.style.SUCCESS('Сходства обновлены успешно'))
