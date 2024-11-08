# файл middleware.py

from django.http import HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect
from django.urls import resolve
from django.http import Http404
import logging
from django.shortcuts import redirect
from urllib.parse import urlparse
from django.shortcuts import get_object_or_404
from .models import Site
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_site(request: HttpRequest) -> Site:
    domain = request.META.get('HTTP_HOST', '')

    if domain == '127.0.0.1:8000':
        domain = 'pragmatic-play.cloud'
    else:
        domain = '.'.join(domain.split('.')[-2:])

    return get_object_or_404(Site, domain=domain)

class CustomRefererMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response
        self.allowed_referer = ['yandex', '127.0.0.1:8000', 'dzen', 'google', 'bing', 'ya.ru', 'mail.ru', 't.me']
        self.useragents = ['yandex', 'google']
        self.blockpage = 'https://yandex.ru/games/'
        self.pass_paths = ['/go/', '/admin/', '/robots.txt', '/sitemap', '/media/', '/static/', '/play/', '/promo/', '/api/']
        self.pass_domains = ['127.0.0.1:8000']


    def __call__(self, request):
        try:

            site = get_site(request)
            self.subdomain = site.redirect_subdomain

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

            # со всех поддоменов отправляем на основной
            # if len(current_host.split('.')) > 2:
            #     return HttpResponsePermanentRedirect("https://" + root + path)
            # else:
            #     return self.get_response(request)


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
                        #return redirect(self.blockpage, permanent=True)
                        return self.render_nginx_page()

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

    def render_nginx_page(self):
        # Здесь вы можете создать и вернуть HTML-страницу
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
        <title>Welcome to nginx!</title>
        <style>
        body{width:35em;margin:0 auto;font-family:Tahoma,Verdana,Arial,sans-serif;}
        </style>
        </head>
        <body>
        <h1>Welcome to nginx!</h1>
        <p>If you see this page, the nginx web server is successfully installed and
        working. Further configuration is required.</p>        
        <p>For online documentation and support please refer to
        <a href="http://nginx.org/">nginx.org</a>.<br/>
        Commercial support is available at
        <a href="http://nginx.com/">nginx.com</a>.</p>       
        <p><em>Thank you for using nginx.</em></p>
        </body></html>
        """
        return HttpResponse(html_content, content_type="text/html")

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
        request.site = get_site(request)
        response = self.get_response(request)
        return response


class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        site = get_site(request)
        domain = site.domain
        # Укажите ваши домены, которые вы хотите разрешить
        allowed_domains = [
            "https://" + domain,    # Замените на ваш первый домен
            "https://" + site.redirect_subdomain + '.' + domain,    # Замените на ваш первый домен
        ]
        # Объединяем домены в строку, разделяя пробелами
        domains_string = ' '.join(allowed_domains)
        response['Content-Security-Policy'] = f"frame-ancestors {domains_string};"
        return response