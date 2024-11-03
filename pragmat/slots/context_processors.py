from django.core.cache import cache
from .models import Theme, Feature, Paylines, get_provider_setting
from pragmatic.models import Language
from django.db.models import Count

def site_context(request):
    current_site = request.site

    # Попробуем получить данные из кеша
    cache_key = f'site_context_{current_site.id}'  # Уникальный ключ кеша для текущего сайта
    context = cache.get(cache_key)

    if context is None:
        # Если данные не найдены в кеше, выполняем запросы к базе данных
        themes = Theme.objects.annotate(slot_count=Count('slot')).filter(
            slot_count__gt=1, slot__provider=current_site.provider
        )

        features = Feature.objects.all()
        paylines = Paylines.objects.all()
        languages = Language.objects.all()

        footer_info = get_provider_setting(current_site.provider, 'footer_info')
        home_page_subtitle = get_provider_setting(current_site.provider, 'home_page_subtitle')
        home_page_info = get_provider_setting(current_site.provider, 'home_page_info')
        slots_list_info = get_provider_setting(current_site.provider, 'slots_list_info')
        feature_1 = get_provider_setting(current_site.provider, 'feature_1')
        feature_2 = get_provider_setting(current_site.provider, 'feature_2')
        feature_3 = get_provider_setting(current_site.provider, 'feature_3')
        keywords = get_provider_setting(current_site.provider, 'keywords')

        # Объединяем данные в словарь
        context = {
            'themes': themes,
            'features': features,
            'paylines': paylines,
            'footer_info': footer_info,
            'home_page_subtitle': home_page_subtitle,
            'home_page_info': home_page_info,
            'slots_list_info': slots_list_info,
            'feature_1': feature_1,
            'feature_2': feature_2,
            'feature_3': feature_3,
            'keywords': keywords,
            'languages': languages,
        }

        # Сохраняем данные в кеш на 15 минут
        cache.set(cache_key, context, timeout=60 * 60 * 24)

    return context
