from django.contrib import admin
from .models import *




class SlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'folk_name', 'sorting_order', 'users_choice', 'is_new', 'is_popular', 'provider')
    search_fields = ['name']
    list_filter = ('provider', )



admin.site.register(Slot, SlotAdmin)
admin.site.register(Image)
admin.site.register(Review)
admin.site.register(Page)
admin.site.register(SlotDescription)