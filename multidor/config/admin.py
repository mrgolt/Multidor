from django.contrib import admin
from .models import Sites, Content, Bonus, Casino

class BonusAdmin(admin.ModelAdmin):
    list_display = ('name', 'casino', 'promo_code', 'referral_link', 'website') # Перечислите поля, которые вы хотите отображать в списке бонусов

    def casino_name(self, obj):
        # Получаем название казино для данного бонуса
        return obj.casino.name if obj.casino else "-"  # Предположим, что поле в модели Bonus для казино называется "casino", а у казино есть поле "name"

admin.site.register(Sites)
admin.site.register(Content)
admin.site.register(Bonus, BonusAdmin)
admin.site.register(Casino)