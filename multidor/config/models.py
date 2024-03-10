from django.db import models

class Sites(models.Model):
    site_id = models.AutoField(primary_key=True)
    allowed_domain = models.CharField(max_length=255)

    def __str__(self):
        return self.allowed_domain

class Casino(models.Model):
    logo = models.ImageField(upload_to='casino_logos/')
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

    def __str__(self):
        return self.title