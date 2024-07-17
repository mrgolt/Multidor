from django.urls import path, re_path
from .views import *
from django.views.generic.base import TemplateView

urlpatterns = [

    path('api/create-site/', create_site, name='create_site'),
    path('api/create-casino/', create_casino, name='create_casino'),
    path('api/create-bonus/', create_bonus, name='create_bonus'),
    path('api/create-content/', create_content, name='create_content'),
    path('api/get-sites/', get_sites, name='get_sites'),
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
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),
    #path('<path:path>', custom_serve),
]