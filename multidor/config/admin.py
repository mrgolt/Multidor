from django.contrib import admin
from .models import *
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

class BonusAdmin(admin.ModelAdmin):
    list_display = ('name', 'casino', 'promo_code', 'referral_link', 'website', 'is_active') # Перечислите поля, которые вы хотите отображать в списке бонусов

    def casino_name(self, obj):
        # Получаем название казино для данного бонуса
        return obj.casino.name if obj.casino else "-"  # Предположим, что поле в модели Bonus для казино называется "casino", а у казино есть поле "name"

class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'site', 'slug', 'is_main')
    def casino_name(self, obj):
        return obj.casino.name if obj.casino else "-"

class SitesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slot_name', 'allowed_domain_link', 'num_content', 'site_id', 'provider_name', 'template_name')
    def num_content(self, obj):
        return obj.content_set.count()  # Подсчитываем количество объектов Content, связанных с текущим экземпляром Sites

    num_content.short_description = 'Number of Content'
    def casino_name(self, obj):
        return obj.casino.name if obj.casino else "-"

    def allowed_domain_link(self, obj):
        if obj.allowed_domain:
            return format_html('<a href="{0}" target="_blank">{0}</a>', obj.allowed_domain)
        return "-"

    allowed_domain_link.short_description = 'Allowed Domain'

class RedirectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'target_url', 'visits')
    def casino_name(self, obj):
        return obj.casino.name if obj.casino else "-"

class ClickAdmin(admin.ModelAdmin):
    list_display = ('site', 'date_clicked', 'redirect')
    list_filter = ('date_clicked', 'site', )





admin.site.register(Sites, SitesAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Bonus, BonusAdmin)
admin.site.register(Casino)
admin.site.register(Redirect, RedirectAdmin)
admin.site.register(Click, ClickAdmin)