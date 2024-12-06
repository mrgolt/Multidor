import openai
from django.core.management.base import BaseCommand
from slots.models import Slot, Theme
from bs4 import BeautifulSoup



class Command(BaseCommand):
    help = 'Назначить тему для слотов на основе названия и первого абзаца описания через ChatGPT'

    def handle(self, *args, **kwargs):
        # Получаем все темы из базы данных
        existing_themes = list(Theme.objects.values_list('title_en', flat=True))

        if not existing_themes:
            self.stdout.write(self.style.ERROR("Нет доступных тем в базе данных."))
            return

        # Получаем все слоты провайдера с id=2 и без темы
        slots = Slot.objects.filter(provider_id=1)

        for slot in slots:
            # Парсим описание как HTML с помощью BeautifulSoup
            soup = BeautifulSoup(slot.description, 'html.parser')

            # Находим первый <p> элемент с длиной текста больше 200 символов
            first_paragraph = None
            for p in soup.find_all('p'):
                if len(p.get_text(strip=True)) > 200:
                    first_paragraph = p.get_text(strip=True)
                    break

            # Если мы нашли подходящий абзац, то продолжаем, иначе пропускаем слот
            if not first_paragraph:
                self.stdout.write(self.style.WARNING(f"Для слота '{slot.name}' нет абзаца с длиной больше 200 символов"))
                continue

            slot_name = slot.name
            description_first_paragraph = first_paragraph

            # Формируем запрос для ChatGPT, чтобы выбрать тему из существующих
            messages = [
                {"role": "system",
                 "content": "You are an assistant that assigns themes to slot games based on their name and description. "
                            "Only respond with a single word from the provided theme list."},
                {"role": "user", "content": (
                    f"На основе названия слота '{slot_name}' и его описания: "
                    f"'{description_first_paragraph}', выбери наиболее подходящую тему "
                    f"из следующего списка: {', '.join(existing_themes)}."
                )}
            ]

            try:
                # Отправляем запрос к OpenAI для получения темы
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",  # Указываем модель
                    messages=messages,
                    max_tokens=50,  # Ограничиваем длину ответа
                    temperature=0.7,  # Температура генерации
                )

                # Получаем результат от ChatGPT
                selected_theme = response['choices'][0]['message']['content'].strip()

                # Проверяем, что выбранная тема существует в списке
                if selected_theme not in existing_themes:
                    self.stdout.write(self.style.WARNING(f"Для слота '{slot.name}' ChatGPT выбрал несуществующую тему: '{selected_theme}'"))
                    continue

                # Назначаем тему слоту
                theme = Theme.objects.get(title_en=selected_theme)
                slot.theme = theme
                slot.save()

                self.stdout.write(self.style.SUCCESS(f"Тема для слота '{slot.name}' обновлена на '{selected_theme}'"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка при получении темы для слота '{slot.name}': {str(e)}"))
