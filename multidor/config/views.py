from django.conf import settings
from django.views.static import serve
from django.shortcuts import render
import os

def custom_serve(request, path, document_root=None, show_indexes=False):
    domain = request.META.get('HTTP_HOST', '')
    file_path = os.path.join(settings.STATICFILES_DIRS[0], domain, path)
    if path.endswith('.css') and os.path.exists(file_path):
        return serve(request, file_path, document_root, show_indexes)
    else:
        template_path = os.path.join(domain, 'main.html')
        return render(request, template_path)

