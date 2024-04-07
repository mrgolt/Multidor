from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class Sites(models.Model):
    name = models.CharField(max_length=200, default='')
    slot_name = models.CharField(max_length=200, default='')
    demo = models.TextField(blank=True, default='')
    provider_name = models.CharField(blank=True, max_length=200, default='')
    site_id = models.AutoField(primary_key=True)
    allowed_domain = models.CharField(blank=True, max_length=255)
    logo = models.ImageField(blank=True, upload_to='img/', default='')
    hero_image = models.ImageField(blank=True, upload_to='img/', default='')
    apk_file = models.FileField(blank=True, upload_to='file/', default='')
    promo_image = models.ImageField(blank=True, upload_to='img/', default='')
    favicon = models.ImageField(blank=True, upload_to='img/', default='')
    yt_link = models.TextField(blank=True, default='')
    tlg_link = models.TextField(blank=True, default='')
    redirect = models.ForeignKey('Redirect', on_delete=models.CASCADE, blank=True)
    counters = models.TextField(blank=True, default='')
    template_name = models.CharField(blank=True, max_length=200, default='main.html')

    def __str__(self):
        return self.allowed_domain

class Casino(models.Model):
    logo = models.ImageField(upload_to='img/', default='cas_logo.jpg')
    name = models.CharField(max_length=100)
    redirect = models.ForeignKey('Redirect', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

class Bonus(models.Model):
    casino = models.ForeignKey('Casino', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    promo_code = models.CharField(max_length=50)
    referral_link = models.URLField()
    website = models.ForeignKey('Sites', on_delete=models.CASCADE)
    redirect = models.ForeignKey('Redirect', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Content(models.Model):
    site = models.ForeignKey('Sites', on_delete=models.CASCADE)
    text = models.TextField()
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, default='')
    is_main = models.BooleanField()


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Преобразовать заголовок в slug
        super().save(*args, **kwargs)

class Redirect(models.Model):
    id = models.AutoField(primary_key=True)
    target_url = models.URLField()
    name = models.CharField(max_length=100, default='')
    visits = models.IntegerField(default=0)
    aff = models.ForeignKey('Aff', on_delete=models.CASCADE, default=1)

    def increment_visits(self):
        """
        Увеличивает счетчик визитов на 1
        """
        self.visits += 1
        self.save()

    def __str__(self):
        return f"{self.name} -> {self.target_url}"

class Click(models.Model):
    redirect = models.ForeignKey('Redirect', on_delete=models.CASCADE)
    site = models.ForeignKey('Sites', on_delete=models.CASCADE)
    date_clicked = models.DateTimeField(default=timezone.now)
    aff = models.ForeignKey('Aff', on_delete=models.CASCADE, default=1)

class Aff(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"{self.name}"

class AffReg(models.Model):
    id = models.AutoField(primary_key=True)
    campaign_id = models.PositiveIntegerField()
    promo_id = models.PositiveIntegerField()
    visit_id = models.CharField(max_length=100)
    player_id = models.PositiveIntegerField()
    click = models.ForeignKey('Click', on_delete=models.CASCADE, blank=True)
    reg_date = models.DateTimeField(default=timezone.now)
    aff = models.ForeignKey('Aff', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.player_id}"

    #https: // sweetbonanza.best / postbackcats / reg /?campaign_id = 237844 & promo_id = 280615 & visit_id = 6610
    #b0c755213525d570e555 & player_id = 19283593 & click_id =

class AffDep(models.Model):
    id = models.AutoField(primary_key=True)
    campaign_id = models.PositiveIntegerField()
    promo_id = models.PositiveIntegerField()
    visit_id = models.CharField(max_length=100)
    player_id = models.PositiveIntegerField()
    amount = models.FloatField()
    amount_cents = models.PositiveIntegerField()
    currency = models.CharField(max_length=100)
    deposit_id = models.PositiveIntegerField()
    click = models.ForeignKey('Click', on_delete=models.CASCADE, blank=True)
    dep_date = models.DateTimeField(default=timezone.now)
    aff = models.ForeignKey('Aff', on_delete=models.CASCADE, default=1)
    is_first = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.deposit_id}"

    #https://sweetbonanza.best/postbackcats/dep/?campaign_id=237844&promo_id=280615&visit_id=66106d7827419a95682f592a&amount=250.00&amount_cents=25000&currency=RUB&deposit_id=44445971&player_id=19275238&click_id=