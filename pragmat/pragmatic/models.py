from django.db import models
from django.core.exceptions import ValidationError

class Provider(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Offer(models.Model):
    redirect_name = models.CharField(max_length=255)
    redirect_url = models.CharField(max_length=255)

    def __str__(self):
        return self.redirect_name

class Site(models.Model):
    domain = models.CharField(max_length=255)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    counters = models.TextField()
    offers = models.ManyToManyField(Offer, blank=True)
    redirect_subdomain = models.CharField(max_length=30, default='www')
    base_template = models.CharField(max_length=50, default='base.html')
    home_template = models.CharField(max_length=50, default='home.html')
    page_detail_template = models.CharField(max_length=50, default='page_detail.html')
    slot_detail_template = models.CharField(max_length=50, default='slot_detail.html')
    slot_list_template = models.CharField(max_length=50, default='slot_list.html')

    def __str__(self):
        return self.domain

class Language(models.Model):
    code = models.CharField(max_length=2, unique=True)  # Код языка (например, 'ru', 'en')
    name = models.CharField(max_length=30)              # Название языка (например, 'Русский', 'English')

    def __str__(self):
        return self.name

class SiteSetting(models.Model):
    site = models.ForeignKey('Site', on_delete=models.CASCADE)  # Сайт, к которому относятся настройки
    name = models.CharField(max_length=255, unique=True)  # Название настройки
    value = models.TextField()  # Значение настройки

    def __str__(self):
        return f"{self.site} - {self.name}"

    class Meta:
        unique_together = ('site', 'name')  # Уникальная пара: сайт и название настройки

    def clean(self):
        """ Ensure no duplicate settings with the same name for the same site """
        if SiteSetting.objects.filter(site=self.site, name=self.name).exclude(id=self.id).exists():
            raise ValidationError(f"Setting with name {self.name} already exists for this site.")


def get_site_setting(site, name):
    try:
        return SiteSetting.objects.get(site=site, name=name).value
    except SiteSetting.DoesNotExist:
        return None

class FAQ(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    language = models.ForeignKey('Language', on_delete=models.CASCADE)

    def __str__(self):
        return self.question