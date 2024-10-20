from django.http import HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect
from django.urls import resolve
from django.http import Http404
import logging
from django.shortcuts import redirect
from urllib.parse import urlparse
from django.shortcuts import get_object_or_404
from .models import Site

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CustomRefererMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_referer = ['yandex', '127.0.0.1:8000', 'dzen', 'google', 'bing', 'ya.ru', 'mail.ru', 't.me']
        self.useragents = ['yandex', 'google']
        self.subdomain = 'ru'
        self.blockpage = 'https://yandex.ru/games/'
        self.pass_paths = ['/go/', '/admin/', '/robots.txt', '/sitemap.xml', '/media/', '/static/']
        self.pass_domains = ['127.0.0.1:8000']


    def __call__(self, request):
        try:
            referer = request.META.get('HTTP_REFERER', '')
            user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
            current_host = request.get_host()
            path = request.META.get('PATH_INFO', '')

            logger.warning(current_host)

            # делаем домен второго уровня
            root = '.'.join(current_host.split('.')[-2:])

            # Если домен технический или path разрешенный, никуда не редиректим, возвращаем исходный запрос
            if any(dm in current_host for dm in self.pass_domains) or any(pt in path for pt in self.pass_paths):
                logger.debug("Если домен технический или path разрешенный")
                return self.get_response(request)

            if len(current_host.split('.')) > 2:
                return HttpResponsePermanentRedirect("https://" + root + path)
            else:
                return self.get_response(request)


            # Если это бот Я или Г, а домен 3 или больше уровня, отправляем на домен второго уровня
            if len(current_host.split('.')) > 2 and any(ua in user_agent for ua in self.useragents):
                logger.debug("если бот - если юа & sub")
                return HttpResponsePermanentRedirect("https://" + root + path)

            # Если не бот и не разрешенный реферер
            if not any(ref in referer for ref in self.allowed_referer) and not any(ua in user_agent for ua in self.useragents):
                # Если поддомен не тот, который указан выше или поддомена нет совсем
                if self.subdomain not in current_host.split('.')[0] or len(current_host.split('.')) == 2:
                    # Если это не техническая страница и не технический домен
                    if not any(pt in path for pt in self.pass_paths) and not any(dm in current_host for dm in self.pass_domains):
                        logger.debug("если прямой - нет реферера нет юа и не наш sub")
                        # Отправляем на левую страницу
                        return redirect(self.blockpage, permanent=True)

            # Если реферер среди разрешенных, это не бот и не технический домен
            if any(ref in referer for ref in self.allowed_referer) and not any(ua in user_agent for ua in self.useragents) and not any(dm in current_host for dm in self.pass_domains):
                # Если поддомен не тот, который указан выше или поддомена нет совсем, отправляем на нужный поддомен
                if self.subdomain not in current_host.split('.')[0] or len(current_host.split('.')) == 2:
                    if len(current_host.split('.')) > 2:
                        way = "https://" + self.subdomain + '.' + root + path
                    else:
                        way = "https://" + self.subdomain + '.' + current_host + path
                    logger.debug("если посетитель - если реферер нет юа " + way)
                    return HttpResponseRedirect(way) #закомментить чтобы можно было войти в админку



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
    
    
    если посетитель - если реферер & нет юа
        если домен != sub.domain
            301 => sub.domain
    
    """



class SiteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        domain = request.META.get('HTTP_HOST', '')

        if domain == '127.0.0.1:8000':
            domain = 'pragmatic-play.cloud'
        else:
            domain = '.'.join(domain.split('.')[-2:])

        request.site = get_object_or_404(Site, domain=domain)

        response = self.get_response(request)
        return response
