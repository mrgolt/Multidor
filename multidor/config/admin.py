from django.contrib import admin
from .models import *
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db.models import Max


class BonusAdmin(admin.ModelAdmin):
    list_display = ('name', 'casino', 'promo_code', 'referral_link', 'website',
                    'is_active')  # Перечислите поля, которые вы хотите отображать в списке бонусов

    def casino_name(self, obj):
        # Получаем название казино для данного бонуса
        return obj.casino.name if obj.casino else "-"  # Предположим, что поле в модели Bonus для казино называется "casino", а у казино есть поле "name"


class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'site', 'slug', 'is_main')

    def casino_name(self, obj):
        return obj.casino.name if obj.casino else "-"


class SitesAdmin(admin.ModelAdmin):
    list_display = (
    'site_id', 'allowed_domain_link', 'slot_name', 'num_content', 'provider_name', 'template_name', 'has_hero_image')

    def num_content(self, obj):
        return obj.content_set.count()  # Подсчитываем количество объектов Content, связанных с текущим экземпляром Sites

    num_content.short_description = 'Pages'

    def casino_name(self, obj):
        return obj.casino.name if obj.casino else "-"

    def allowed_domain_link(self, obj):
        if obj.allowed_domain:
            return format_html('<a href="https://{0}/" target="_blank">{0}</a>', obj.allowed_domain)
        return "-"

    allowed_domain_link.short_description = 'Domain'

    def has_hero_image(self, obj):
        return obj.hero_image != ''

    has_hero_image.boolean = True
    has_hero_image.short_description = 'Has Hero'


class RedirectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'aff', 'target_url', 'visits')

    def casino_name(self, obj):
        return obj.casino.name if obj.casino else "-"


class ClickAdmin(admin.ModelAdmin):
    list_display = ('id', 'ref_site', 'date_clicked', 'redirect', 'click_count')
    list_filter = ('date_clicked', 'site')

    def ref_site(self, obj):
        return obj.site.allowed_domain

    def click_count(self, obj):
        request = self.request
        date_clicked__gte = request.GET.get('date_clicked__gte', '')
        date_clicked__lt = request.GET.get('date_clicked__lt', '')

        filter_kwargs = {'site': obj.site}
        if date_clicked__gte:
            filter_kwargs['date_clicked__gte'] = date_clicked__gte
        if date_clicked__lt:
            filter_kwargs['date_clicked__lt'] = date_clicked__lt

        click_count = Click.objects.filter(**filter_kwargs).aggregate(count=Count('id')).get('count', 0)
        return click_count

    def changelist_view(self, request, extra_context=None):
        self.request = request
        return super().changelist_view(request, extra_context)

    def get_queryset(self, request):
        #unique_site_ids = Click.objects.values_list('site_id', flat=True).distinct()
        clicks = Click.objects.all().values('site_id').distinct()
        #print(Click.objects.all())
        return Click.objects.all()

    ref_site.short_description = 'Site'
    click_count.short_description = 'Clicks from domain'


class AffAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Sites, SitesAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Bonus, BonusAdmin)
admin.site.register(Casino)
admin.site.register(Redirect, RedirectAdmin)
admin.site.register(Click, ClickAdmin)
admin.site.register(Aff, AffAdmin)
