from django.shortcuts import render
import os
from .models import Sites

def custom_serve(request):
    domain = request.META.get('HTTP_HOST', '')
    try:
        site = Sites.objects.get(allowed_domain=domain)
        print(domain)
    except Sites.DoesNotExist:
        site = None

    template_path = os.path.join(domain, 'main.html')
    return render(request, template_path, {'site': site})