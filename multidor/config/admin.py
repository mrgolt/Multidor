from django.contrib import admin
from .models import Sites, Templates

@admin.register(Sites)
class SitesAdmin(admin.ModelAdmin):
    list_display = ('site_id', 'allowed_domain')
    search_fields = ('site_id', 'allowed_domain')

@admin.register(Templates)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_id')