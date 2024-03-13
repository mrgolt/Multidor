from django.shortcuts import render
import os
from config.models import Sites, Bonus, Content

def custom_serve(request):
    domain = request.META.get('HTTP_HOST', '')

    if domain == '127.0.0.1:8000':
        domain = 'sweetbonanza.best'

    try:
        site = Sites.objects.filter(allowed_domain=domain)[0]
        bonuses = Bonus.objects.filter(website=site)
        content = Content.objects.filter(is_main=True, site=site)
    except Sites.DoesNotExist:
        site = None

    template_path = os.path.join(domain, 'main.html')

    return render(request, template_path, {'site': site, 'bonuses': bonuses, 'content': content})