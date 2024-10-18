from .models import Theme, Feature, Paylines
from django.db.models import Count

def themes(request):
    # Получаем текущий сайт из запроса
    current_site = request.site

    # Фильтруем темы, которые связаны с текущим сайтом через слоты
    themes = Theme.objects.annotate(slot_count=Count('slot')).filter(
        slot_count__gt=1, slot__provider=current_site.provider
    )

    return {'themes': themes}

def features(request):
    features = Feature.objects.all()
    return {'features': features}

def paylines(request):
    paylines = Paylines.objects.all()
    return {'paylines': paylines}