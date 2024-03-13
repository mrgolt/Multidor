from django.shortcuts import render
import os
from config.models import Sites, Bonus, Content

def custom_serve(request):
    domain = request.META.get('HTTP_HOST', '')
    try:
        site = Sites.objects.first()
        bonuses = Bonus.objects.all()
        content = Content.objects.filter(is_main=True)
    except Sites.DoesNotExist:
        site = None

    if domain == '127.0.0.1:8000':
        domain = 'sweetbonanza.best'

    template_path = os.path.join(domain, 'main.html')

    return render(request, template_path, {'site': site, 'bonuses': bonuses, 'content': content})