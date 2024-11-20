from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_index_now_request

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    short_bio = models.TextField(default='', blank=True)
    bio = models.TextField(default='', blank=True)
    photo = models.ImageField(upload_to='authors/', null=True, blank=True)
    position = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Sites(models.Model):

    TYPE_CHOICES = [
        ('slot', 'Slot'),
        ('casino', 'Casino'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='slot')
    name = models.CharField(max_length=200, default='')
    slot_name = models.CharField(max_length=200, default='')
    demo = models.TextField(blank=True, default='')
    provider_name = models.CharField(blank=True, max_length=200, default='')
    provider_description = models.TextField(blank=True, default='')
    site_id = models.AutoField(primary_key=True)
    allowed_domain = models.CharField(blank=True, max_length=255)
    logo = models.ImageField(blank=True, upload_to='img/', default='')
    logo_svg = models.FileField(blank=True, upload_to='img/')
    hero_image = models.ImageField(blank=True, upload_to='img/', default='')
    hero_image_is_rounded = models.BooleanField(default=False)
    apk_file = models.FileField(blank=True, upload_to='file/', default='')
    promo_image = models.ImageField(blank=True, upload_to='img/', default='')
    interface_image = models.ImageField(blank=True, upload_to='interface-img/', default='')
    interface_image_webp = models.FileField(blank=True, upload_to='img/')
    favicon = models.ImageField(blank=True, upload_to='img/', default='')
    favicon_file = models.FileField(blank=True, upload_to='favicon/')
    css_file = models.FileField(blank=True, upload_to='css/', default='css/dark.min.css')
    yt_link = models.TextField(blank=True, default='')
    tlg_link = models.TextField(blank=True, default='')
    counters = models.TextField(blank=True, default='')
    template_name = models.CharField(blank=True, max_length=200, default='main.html')
    custom_css = models.TextField(blank=True, default='')
    background_color_primary = models.CharField(max_length=10, default='#1a0e1e', blank=True)
    background_color_secondary = models.CharField(max_length=10, default='#33263a', blank=True)
    primary_color = models.CharField(max_length=10, default='darksalmon', blank=True)
    secondary_color = models.CharField(max_length=10, default='#48c78e', blank=True)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, default=None, null=True, blank=True)
    casino = models.ForeignKey('Casino', on_delete=models.CASCADE, null=True, blank=True)
    slot_rtp = models.CharField(max_length=10, default='98.96', null=True, blank=True)

    def __str__(self):
        return self.allowed_domain

class Casino(models.Model):
    logo = models.ImageField(upload_to='img/', default='cas_logo.jpg')
    logo_svg = models.FileField(upload_to='img/', default='logo.svg', validators=[FileExtensionValidator(['svg', 'webp'])])
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100, blank=True)
    alternative_name = models.CharField(max_length=100, blank=True)
    redirect = models.ForeignKey('Redirect', on_delete=models.CASCADE, default=1)
    custom_css = models.TextField(blank=True)
    favicon = models.FileField(upload_to='favicons/', default='favicon.ico', validators=[FileExtensionValidator(['ico', 'png', 'svg', 'webp'])])

    def __str__(self):
        return self.name

class Bonus(models.Model):
    casino = models.ForeignKey('Casino', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    promo_code = models.CharField(max_length=50)
    referral_link = models.URLField()
    website = models.ForeignKey('Sites', on_delete=models.CASCADE)
    redirect = models.ForeignKey('Redirect', on_delete=models.CASCADE)
    sorting_order = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Symbol(models.Model):
    info = models.TextField()
    name = models.CharField(max_length=100, blank=True, default='')
    website = models.ForeignKey('Sites', on_delete=models.CASCADE)
    sorting_order = models.PositiveIntegerField(default=20)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(blank=True, upload_to='img/', default='')

    def __str__(self):
        return self.name



class FAQ(models.Model):
    content = models.ForeignKey('Content', on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'Вопрос "{self.question}" к странице "{self.content}"'


class Content(models.Model):
    site = models.ForeignKey('Sites', on_delete=models.CASCADE)
    text = models.TextField()
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    demo = models.TextField(blank=True)
    description = models.TextField()
    keywords = models.CharField(max_length=1000)
    slug = models.CharField(max_length=255, default='')
    is_main = models.BooleanField()
    is_popular = models.BooleanField(default=True)
    is_version_page = models.BooleanField(default=False)
    interface_image = models.ImageField(blank=True, upload_to='interface-img/', default='')


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Преобразовать заголовок в slug
        super().save(*args, **kwargs)

class Image(models.Model):
    title = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=500, blank=True)
    site = models.ForeignKey('Sites', on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='img/', default='')
    in_gallery = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Redirect(models.Model):
    id = models.AutoField(primary_key=True)
    target_url = models.URLField()
    name = models.CharField(max_length=100, default='')
    visits = models.IntegerField(default=0)
    aff = models.ForeignKey('Aff', on_delete=models.CASCADE, default=1)
    site = models.ForeignKey('Sites', on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=100, default='CPA', blank=True, null=True)

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



class GamblingResource(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    url = models.URLField()
    info = models.TextField()
    is_active = models.BooleanField(default=True)
    logo = models.ImageField(blank=True, upload_to='gambling-resources-img/', default='')

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=False)
    page = models.ForeignKey('Content', on_delete=models.CASCADE)

@receiver(post_save, sender=Content)
def index_object(sender, instance, **kwargs):
    if instance.is_main == False:
        url = f'https://{instance.site.allowed_domain}/page/{instance.slug}/'
    else:
        url = f'https://{instance.site.allowed_domain}/'
    #print(url)
    resp = send_index_now_request(url)
    print(resp)