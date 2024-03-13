from django.db import models

class Sites(models.Model):
    name = models.CharField(max_length=200, default='doghouse.best')
    slot_name = models.CharField(max_length=200, default='The Dog House')
    demo = models.TextField(default='')
    provider_name = models.CharField(max_length=200, default='Pragmatic Play')
    site_id = models.AutoField(primary_key=True)
    allowed_domain = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='img/', default='logo.jpg')
    hero_image = models.ImageField(upload_to='img/', default='hero.jpg')
    apk_file = models.FileField(upload_to='file/', default='default_apk.apk')
    promo_image = models.ImageField(upload_to='img/', default='promo.jpg')

    def __str__(self):
        return self.allowed_domain

class Casino(models.Model):
    logo = models.ImageField(upload_to='img/', default='cas_logo.jpg')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Bonus(models.Model):
    casino = models.ForeignKey('Casino', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    promo_code = models.CharField(max_length=50)
    referral_link = models.URLField()
    website = models.ForeignKey('Sites', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Content(models.Model):
    site = models.ForeignKey('Sites', on_delete=models.CASCADE)
    text = models.TextField()
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.CharField(max_length=255)
    is_main = models.BooleanField()

    def __str__(self):
        return self.title