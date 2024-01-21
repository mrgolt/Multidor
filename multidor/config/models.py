from django.db import models

class Sites(models.Model):
    site_id = models.AutoField(primary_key=True)
    allowed_domain = models.CharField(max_length=255)

class Templates(models.Model):
    template_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    template_file = models.FileField(upload_to='template_files/', null=True, blank=True)