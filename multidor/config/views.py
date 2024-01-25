from django.conf import settings
from django.views.static import serve
from django.shortcuts import render
from django.http import HttpResponse
import os

def custom_serve(request, document_root=None, show_indexes=False):
    print(request)
    path = request.path
    domain = request.META.get('HTTP_HOST', '')
    file_path = os.path.join(settings.STATICFILES_DIRS[0], domain, path)
    _, extension = os.path.splitext(file_path)
    if extension:
        if os.path.exists(file_path):
            return serve(request, file_path, document_root, show_indexes)
        else:
            return HttpResponse(status=404)
    else:
        template_path = os.path.join(domain, 'main.html')
        return render(request, template_path)

