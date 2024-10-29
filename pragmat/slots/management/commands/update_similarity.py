# slots/management/commands/update_similarity.py
from django.core.management.base import BaseCommand
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from slots.models import Slot
import numpy as np


class Command(BaseCommand):
    help = 'Обновление косинусного сходства для похожих слотов'

    def handle(self, *args, **kwargs):
        slots = Slot.objects.all()
        texts = [f"{slot.name} {slot.description}" for slot in slots]

        # Векторизация текста
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(texts)

        # Вычисление косинусного сходства
        cosine_similarities = cosine_similarity(tfidf_matrix)

        # Обновление похожих слотов
        for idx, slot in enumerate(slots):
            similar_indices = cosine_similarities[idx].argsort()[-11:-1][::-1]  # 5 самых похожих
            similar_slots_ids = [slots[int(i)].id for i in similar_indices]  # Преобразуем i в int
            slot.similar_slots = similar_slots_ids
            slot.save()

        self.stdout.write(self.style.SUCCESS('Сходства обновлены успешно'))
