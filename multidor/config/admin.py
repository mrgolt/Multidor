from django.contrib import admin
from .models import Sites, Content, Bonus, Casino, Redirect

class BonusAdmin(admin.ModelAdmin):
    list_display = ('name', 'casino', 'promo_code', 'referral_link', 'website') # Перечислите поля, которые вы хотите отображать в списке бонусов

    def casino_name(self, obj):
        # Получаем название казино для данного бонуса
        return obj.casino.name if obj.casino else "-"  # Предположим, что поле в модели Bonus для казино называется "casino", а у казино есть поле "name"

class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'site', 'slug', 'is_main')
    def casino_name(self, obj):
        return obj.casino.name if obj.casino else "-"

class SitesAdmin(admin.ModelAdmin):
    list_display = ('name', 'allowed_domain', 'site_id')
    def casino_name(self, obj):
        return obj.casino.name if obj.casino else "-"

class RedirectAdmin(admin.ModelAdmin):
    list_display = ('id', 'target_url', 'name')
    def casino_name(self, obj):
        return obj.casino.name if obj.casino else "-"

admin.site.register(Sites, SitesAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Bonus, BonusAdmin)
admin.site.register(Casino)
admin.site.register(Redirect, RedirectAdmin)