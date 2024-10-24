from .models import Theme, Feature, Paylines, get_provider_setting
from django.db.models import Count

def site_context(request):
    current_site = request.site

    # Получение тем, связанных со слотами текущего сайта
    themes = Theme.objects.annotate(slot_count=Count('slot')).filter(
        slot_count__gt=1, slot__provider=current_site.provider
    )

    # Получение всех доступных Features
    features = Feature.objects.all()

    # Получение всех доступных Paylines
    paylines = Paylines.objects.all()

    # Получение информации из настройки провайдера
    footer_info = get_provider_setting(current_site.provider, 'footer_info')
    home_page_subtitle = get_provider_setting(current_site.provider, 'home_page_subtitle')
    home_page_info = get_provider_setting(current_site.provider, 'home_page_info')
    slots_list_info = get_provider_setting(current_site.provider, 'slots_list_info')

    # Возвращаем объединенный словарь контекста
    return {
        'themes': themes,
        'features': features,
        'paylines': paylines,
        'footer_info': footer_info,
        'home_page_subtitle': home_page_subtitle,
        'home_page_info': home_page_info,
        'slots_list_info': slots_list_info,
    }