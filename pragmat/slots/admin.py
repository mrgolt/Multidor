from django.contrib import admin
from .models import *

class SlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'version', 'folk_name', 'sorting_order', 'users_choice', 'is_new', 'is_popular', 'provider', 'slot_type', 'theme', 'updated_at', 'similar_slots', 'logo')
    search_fields = ['name']
    list_filter = ('provider', )

class SlotDescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'slot', 'site', 'language')
    search_fields = ['slot', 'site', 'language']
    list_filter = ('site', 'language')

class ProviderSettingAdmin(admin.ModelAdmin):
    list_display = ('provider', 'name', 'value')
    search_fields = ('name', 'value')

class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ru', 'title_en', 'title_es', 'title_pt', 'title_de')

admin.site.register(ProviderSetting, ProviderSettingAdmin)
admin.site.register(Slot, SlotAdmin)
admin.site.register(Image)
admin.site.register(Review)
admin.site.register(Page)
admin.site.register(SlotDescription, SlotDescriptionAdmin)
admin.site.register(SlotType)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Feature)
admin.site.register(Paylines)