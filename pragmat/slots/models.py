from django.db import models
from autoslug import AutoSlugField


class Slot(models.Model):
    name = models.CharField(max_length=100, unique=True)
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