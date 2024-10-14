from django.db import models
from autoslug import AutoSlugField
from pragmatic.models import Provider, Site

class SlotType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Theme(models.Model):
    title = models.CharField(max_length=100, unique=True)
    russian_title = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True, editable=True)

    def __str__(self):
        return self.title

class Feature(models.Model):
    title = models.CharField(max_length=100, unique=True)
    russian_title = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True, editable=True)

    def __str__(self):
        return self.title

class Paylines(models.Model):
    title = models.CharField(max_length=100, unique=True)
    russian_title = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True, editable=True)

    def __str__(self):
        return self.title

class Slot(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=100, default='1.0.0')
    folk_name = models.CharField(max_length=100, blank=True, default='')
    game_symbol = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='slot_logos/')
    description = models.TextField(blank=True)
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
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True)
    paylines = models.ForeignKey(Paylines, on_delete=models.SET_NULL, null=True)
    features = models.ManyToManyField(Feature, blank=True)

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

class Page(models.Model):
    title = models.CharField(max_length=300, unique=True)
    description = models.TextField(blank=True)
    slug = AutoSlugField(populate_from='title', unique=True, editable=True)

    def __str__(self):
        return self.title

class SlotDescription(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    snippet = models.TextField(blank=True)

    def __str__(self):
        return f"{self.site} - {self.slot}"


