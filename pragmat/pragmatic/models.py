from django.db import models


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
    offers = models.ManyToManyField(Offer, blank=True)
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
