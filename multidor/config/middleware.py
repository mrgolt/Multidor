from django.http import HttpResponseRedirect
from django.urls import resolve
from django.http import Http404
from .models import Redirect

class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith('/go/'):
            redirect_id = request.path.split('/go/')[1]

            try:
                redirect_obj = Redirect.objects.get(id=redirect_id)
            except Redirect.DoesNotExist:
                raise Http404("Redirect does not exist")

            target_url = redirect_obj.target_url

            return HttpResponseRedirect(target_url)

        return response
