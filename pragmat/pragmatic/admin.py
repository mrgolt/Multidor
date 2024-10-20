from django.contrib import admin
from .models import Provider, Site, Offer, Language


class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'provider',)
    search_fields = ['domain', 'provider']
    list_filter = ('provider',)


class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'redirect_name', 'redirect_url',)
    search_fields = ['redirect_name', 'redirect_url']

admin.site.register(Provider)
admin.site.register(Site, SiteAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Language)
