from django.db import models
from autoslug import AutoSlugField
from pragmatic.models import Provider, Site, Language
from django.utils.translation import get_language
from django.core.exceptions import ValidationError

class SlotType(models.Model):
    name = models.CharField(max_length=100)
    plural = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Theme(models.Model):
    title_en = models.CharField(max_length=100, unique=True, blank=True)
    title_ru = models.CharField(max_length=100, unique=True, blank=True)
    title_de = models.CharField(max_length=100, blank=True)
    title_pt = models.CharField(max_length=100, blank=True)
    title_es = models.CharField(max_length=100, blank=True)
    slug = AutoSlugField(populate_from='title_en', unique=True, editable=True)

    def __str__(self):
        return self.title_ru

    def title(self):
        lang = get_language()
        titles = {
            'ru': self.title_ru,
            'en': self.title_en,
            'de': self.title_de,
            'pt': self.title_pt,
            'es': self.title_es,
        }
        title_value = titles.get(lang, None)

        if not title_value:
            return self.title_en

        return title_value

class Feature(models.Model):
    title_en = models.CharField(max_length=100, unique=True, blank=True)
    title_ru = models.CharField(max_length=100, unique=True, blank=True)
    title_de = models.CharField(max_length=100, blank=True)
    title_pt = models.CharField(max_length=100, blank=True)
    title_es = models.CharField(max_length=100, blank=True)
    slug = AutoSlugField(populate_from='title_en', unique=True, editable=True)

    def __str__(self):
        return self.title_ru

class Paylines(models.Model):
    title_en = models.CharField(max_length=100, unique=True, blank=True)
    title_ru = models.CharField(max_length=100, unique=True, blank=True)
    title_de = models.CharField(max_length=100, blank=True)
    title_pt = models.CharField(max_length=100, blank=True)
    title_es = models.CharField(max_length=100, blank=True)
    slug = AutoSlugField(populate_from='title_en', unique=True, editable=True)

    def __str__(self):
        return self.title_ru

class Slot(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=100, default='1.0.0')
    folk_name = models.CharField(max_length=100, blank=True, default='')
    game_symbol = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='slot_logos/')
    description = models.TextField(blank=True)
    context = models.TextField(blank=True)
    snippet = models.TextField(blank=True)
    slug = AutoSlugField(populate_from='name', unique=True, null=True, blank=True)
    rtp = models.FloatField()
    rating = models.FloatField()
    users_choice = models.BooleanField(default=False)
    sorting_order = models.FloatField(blank=True)
    is_new = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, default=1)
    slot_type = models.ForeignKey(SlotType, on_delete=models.SET_NULL, null=True, default=1)
    updated_at = models.DateTimeField(auto_now=True)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True)
    paylines = models.ForeignKey(Paylines, on_delete=models.SET_NULL, null=True, blank=True)
    features = models.ManyToManyField(Feature, blank=True)
    similar_slots = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title


class Review(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    username = models.CharField(max_length=255)
    rating = models.FloatField()

    def __str__(self):
        return f"Review by {self.username} for {self.slot.name}"

from django.utils.translation import get_language
from django.db import models
from autoslug import AutoSlugField

class Page(models.Model):
    slug = AutoSlugField(populate_from='title_en', unique=True, editable=True)

    title_en = models.CharField(max_length=200, blank=True)
    title_ru = models.CharField(max_length=200, blank=True)
    title_de = models.CharField(max_length=200, blank=True)
    title_pt = models.CharField(max_length=200, blank=True)
    title_es = models.CharField(max_length=200, blank=True)

    description_en = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    description_de = models.TextField(blank=True)
    description_pt = models.TextField(blank=True)
    description_es = models.TextField(blank=True)

    def title(self):
        lang = get_language()
        titles = {
            'ru': self.title_ru,
            'en': self.title_en,
            'de': self.title_de,
            'pt': self.title_pt,
            'es': self.title_es,
        }
        return titles.get(lang, self.title_en)

    def description(self):
        lang = get_language()
        descriptions = {
            'ru': self.description_ru,
            'en': self.description_en,
            'de': self.description_de,
            'pt': self.description_pt,
            'es': self.description_es,
        }
        return descriptions.get(lang, self.description_en)

    def __str__(self):
        return self.title()


class SlotDescription(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    snippet = models.TextField(blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, default=2)

    def __str__(self):
        return f"{self.site} - {self.slot}  - {self.language}"

class ProviderSetting(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)  # Провайдер, к которому относятся настройки
    name = models.CharField(max_length=255, unique=True)  # Название настройки
    value_ru = models.TextField()  # Значение настройки
    value_en = models.TextField()  # Значение настройки
    value_es = models.TextField()  # Значение настройки
    value_de = models.TextField()  # Значение настройки
    value_pt = models.TextField()  # Значение настройки

    def value(self):
        lang = get_language()
        values = {
            'ru': self.value_ru,
            'en': self.value_en,
            'de': self.value_de,
            'pt': self.value_pt,
            'es': self.value_es,
        }
        return values.get(lang, self.value_en)

    def __str__(self):
        return f"{self.provider} - {self.name}"

    class Meta:
        unique_together = ('provider', 'name')  # Уникальная пара: сайт и название настройки

    def clean(self):
        """ Ensure no duplicate settings with the same name for the same site """
        if ProviderSetting.objects.filter(provider=self.provider, name=self.name).exclude(id=self.id).exists():
            raise ValidationError(f"Setting with name {self.name} already exists for this site.")


def get_provider_setting(provider, name):
    try:
        return ProviderSetting.objects.get(provider=provider, name=name).value
    except ProviderSetting.DoesNotExist:
        return None

