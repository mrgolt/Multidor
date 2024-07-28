from django.http import HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect
from django.urls import resolve
from django.http import Http404
from .models import Redirect
import logging
from django.shortcuts import redirect
from urllib.parse import urlparse

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# class SaveHeadersMiddleware:
#     def process_response(self, request, response):
#         # Проверяем, является ли ответ редиректом
#         if isinstance(response, HttpResponseRedirect):
#             # Создаем копию заголовков исходного запроса
#             headers = {key: value for key, value in request.headers.items()}
#             # Добавляем заголовки к новому запросу
#             for key, value in headers.items():
#                 response[key] = value
#         return response

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
                raise Http404("Url does not exist")

            target_url = redirect_obj.target_url

            return HttpResponseRedirect(target_url)

        return response


class CustomRefererMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_referer = ['yandex', '127.0.0.1:8000', 'dzen', 'google', 'bing', 'ya.ru', 'mail.ru', 't.me']
        self.useragents = ['yandex', 'google']
        self.subdomain = 'play'
        self.blockpage = 'https://yandex.ru/games/'
        self.pass_paths = ['/go/', '/admin/', '/all-stats/', '/robots.txt', '/sitemap.xml', '/media/', '/static/', '/offlineconv/']
        #self.pass_domains = ['gatesofolympus.best', 'sugar-rush.best', 'sweetbonanza.best']
        self.pass_domains = ['127.0.0.1:8000']


    def __call__(self, request):
        try:
            referer = request.META.get('HTTP_REFERER', '')
            user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
            current_host = request.get_host()
            path = request.META.get('PATH_INFO', '')
            # logger.debug(f"referer {referer}")
            # logger.debug(f"user_agent {user_agent}")
            # logger.debug(f"host {current_host}")

            # self.allowed_referer.append(f'https://{current_host}/')
            # self.allowed_referer.append(f'https://{self.subdomain}.{current_host}/')

            root_host = current_host.split('.')
            if len(root_host) > 2 and any(ua in user_agent for ua in self.useragents):
                logger.debug("если бот - если юа & sub")
                new_host = '.'.join(current_host.split('.')[1:])
                return HttpResponsePermanentRedirect("https://"+new_host+path)

            if not any(ref in referer for ref in self.allowed_referer) and not any(ua in user_agent for ua in self.useragents):
                if self.subdomain != current_host.split('.')[0]:
                    logger.debug("если прямой - нет реферера нет юа")
                    return redirect(self.blockpage, permanent=True)


            if any(ref in referer for ref in self.allowed_referer) and not any(ua in user_agent for ua in self.useragents):
                logger.debug("если посетитель - если реферер нет юа")
                redirect_url = self._build_redirect_url(request)
                return redirect(redirect_url)



        except Exception as e:
            logger.error(f"An error occurred: {e}")

        return self.get_response(request)

    def _build_redirect_url(self, request):
        parsed_url = urlparse(request.build_absolute_uri())
        netloc = f"{self.subdomain}.{parsed_url.hostname.split('.')[-2]}.{parsed_url.hostname.split('.')[-1]}"
        redirect_url = parsed_url._replace(netloc=netloc, scheme='https').geturl()
        return redirect_url

    def _redirect_with_headers(self, request, new_url):
        response = redirect(new_url, permanent=True)
        for key, value in request.META.items():
            response[key] = value
        return response


    """
    
    если бот - если юа 
        если домен != domain
            301 => domain
    
    +
    если прямой - нет реферера нет юа
        если домен != sub.domain
            301 => white
    
    
    если посетитель - если реферер нет юа
        если домен != sub.domain
            301 => domain
    
    """