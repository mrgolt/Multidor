from django.contrib import admin
from .models import Provider, Site, Offer, Language, SiteSetting, FAQ

class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'provider',)
    search_fields = ['domain', 'provider']
    list_filter = ('provider',)

class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'redirect_name', 'redirect_url',)
    search_fields = ['redirect_name', 'redirect_url']

class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site', 'name', 'value')
    search_fields = ('name', 'value')

class FaqAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'provider', 'language')
    search_fields = ('provider', 'language')
    list_filter = ('provider', 'language')

admin.site.register(SiteSetting, SiteSettingAdmin)
admin.site.register(Provider)
admin.site.register(Site, SiteAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Language)
admin.site.register(FAQ, FaqAdmin)
