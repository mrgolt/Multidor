from .models import Theme, Feature, Paylines
from django.db.models import Count

def themes(request):
    themes = Theme.objects.annotate(slot_count=Count('slot')).filter(slot_count__gt=1)
    return {'themes': themes}

def features(request):
    features = Feature.objects.all()
    return {'features': features}

def paylines(request):
    paylines = Paylines.objects.all()
    return {'paylines': paylines}