from django.urls import path, re_path
from .views import *

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
    path('', custom_serve),
    #path('<path:path>', custom_serve),
]