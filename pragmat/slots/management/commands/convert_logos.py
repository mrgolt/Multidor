import os
from django.core.files import File
from django.core.management.base import BaseCommand
from PIL import Image
from slots.models import Slot  # Замените 'yourapp' на имя вашего приложения

class Command(BaseCommand):
    help = 'Convert PNG logos to WebP and update the Slot model'

    def handle(self, *args, **kwargs):
        # slots = Slot.objects.all()
        slots = Slot.objects.filter(provider_id=1)
        for slot in slots:
            if slot.logo:
                # Открываем изображение
                img_path = slot.logo.path
                img = Image.open(img_path)

                # Сжимаем и сохраняем в формате WebP
                webp_path = os.path.splitext(img_path)[0] + '.webp'
                img.save(webp_path, 'WEBP', quality=80)  # Установите нужное значение качества

                # Обновляем поле logo в модели Slot
                with open(webp_path, 'rb') as webp_file:
                    django_file = File(webp_file)
                    slot.logo.save(os.path.basename(webp_path), django_file, save=True)

                # Удаляем старый файл PNG, если нужно
                if os.path.exists(img_path):
                    os.remove(img_path)

                self.stdout.write(self.style.SUCCESS(f'Successfully converted {slot.name} to WebP.'))
            else:
                self.stdout.write(self.style.WARNING(f'Slot {slot.name} has no logo.'))
