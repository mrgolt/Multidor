from django.conf import settings
from django.views.static import serve
from django.shortcuts import render
from django.http import HttpResponse
import os

def custom_serve(request):
    domain = request.META.get('HTTP_HOST', '')

    template_path = os.path.join(domain, 'main.html')
    return render(request, template_path)