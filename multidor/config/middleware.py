from django.http import HttpResponseRedirect
from django.urls import resolve
from django.http import Http404
from .models import Redirect
import logging
from django.shortcuts import redirect
from urllib.parse import urlparse

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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


class CustomRefererMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_referer = ['https://yandex.ru/', 'https://127.0.0.1:8000/', 'https://dzen.ru/', 'https://google.com/', 'https://www.bing.com/']
        self.useragents = ['yandex', 'google']
        self.subdomain = 'www1'
        self.blockpage = 'https://google.com/'
        self.pass_paths = ['/go/', '/admin/']
        self.pass_domains = ['gatesofolympus.best', 'sugar-rush.best', 'sweetbonanza.best']


    def __call__(self, request):
        try:
            referer = request.META.get('HTTP_REFERER', '')
            user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
            current_host = request.get_host()
            path = request.META.get('PATH_INFO', '')
            logger.debug(f"referer {referer}")
            logger.debug(f"user_agent {user_agent}")
            logger.debug(f"host {current_host}")

            self.allowed_referer.append(f'https://{current_host}/')
            self.allowed_referer.append(f'https://{self.subdomain}.{current_host}/')

            if current_host.startswith(self.subdomain + '.') or any(ua in user_agent for ua in self.useragents) or any(pt in path for pt in self.pass_paths) or current_host in self.pass_domains:
                logger.debug("Already on subdomain or bot, skipping filtering")
                return self.get_response(request)

            else:

                if referer in self.allowed_referer and not any(ua in user_agent for ua in self.useragents):
                    redirect_url = self._build_redirect_url(request)
                    logger.debug(f"Redirecting to {redirect_url} because of valid referer {referer}")
                    return redirect(redirect_url)

                if referer not in self.allowed_referer and not any(ua in user_agent for ua in self.useragents):
                    logger.debug(f"Redirecting to {self.blockpage} because direct visit")
                    return redirect(self.blockpage)

        except Exception as e:
            logger.error(f"An error occurred: {e}")

        return self.get_response(request)

    def _build_redirect_url(self, request):
        parsed_url = urlparse(request.build_absolute_uri())
        netloc = f"{self.subdomain}.{parsed_url.hostname}"
        redirect_url = parsed_url._replace(netloc=netloc).geturl()
        return redirect_url