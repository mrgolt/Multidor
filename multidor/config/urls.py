from django.urls import path, re_path
from .views import *
from django.views.generic.base import TemplateView

class RobotsView(TemplateView):
    template_name = "robots.txt"
    content_type = "text/plain"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем домен из запроса
        request = self.request
        domain = request.get_host()  # Получаем домен
        context['sitemap_url'] = f'https://{domain}/sitemap.xml'
        return context

urlpatterns = [

    path('api/create-site/', create_site, name='create_site'),
    path('api/create-casino/', create_casino, name='create_casino'),
    path('api/create-bonus/', create_bonus, name='create_bonus'),
    path('api/create-content/', create_content, name='create_content'),
    path('api/create-image/', create_image, name='create_image'),
    path('api/contents/', get_contents, name='get_contents'),
    path('api/casinos/', get_casinos, name='get_casinos'),
    path('api/casinos/search/<str:name>/', get_casino_by_name, name='get_casino_by_name'),
    path('api/sites/search/<str:name>/', get_site_by_name, name='get_site_by_name'),
    path('api/sites/', get_sites, name='get_sites'),
    path('api/images/', get_images, name='get_images'),
    path('api/update-site/<int:site_id>/', update_site, name='update_site'),
    path('api/update-site-field/<int:site_id>/', update_site_field, name='update_site_field'),
    path('go/<str:redirect_id>/', redirect_view, name='redirect_view'),
    path('page/<slug:slug>/', custom_serve, name='inner_page'),
    path('postbackcats/reg/', postbackcats_reg, name='postbackcats_reg'),
    path('postbackcats/dep/', postbackcats_dep, name='postbackcats_dep'),
    path('offlineconv/', offlineconv, name='offlineconv'),
    path('sitemap.xml', sitemap_generator, name='sitemap_generator'),
    path('all-stats/', all_stats, name='all_stats'),
    path('', custom_serve),
    path("robots.txt", RobotsView.as_view()),
    path('yandex_<str:code>.html', yandex_webmaster_approve, name='yandex_webmaster_approve'),
    path('<str:indexnow_key>.txt', index_now, name='index_now'),
    path('index_now/', send_index_now, name='send_index_now'),
]