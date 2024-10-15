from .models import Theme, Feature, Paylines

def themes(request):
    themes = Theme.objects.all()
    return {'themes': themes}

def features(request):
    features = Feature.objects.all()
    return {'features': features}

def paylines(request):
    paylines = Paylines.objects.all()
    return {'paylines': paylines}