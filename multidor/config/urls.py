from django.urls import path, re_path
from .views import custom_serve, create_site, create_casino, create_bonus, create_content, redirect_view

urlpatterns = [

    path('api/create-site/', create_site, name='create_site'),
    path('api/create-casino/', create_casino, name='create_casino'),
    path('api/create-bonus/', create_bonus, name='create_bonus'),
    path('api/create-content/', create_content, name='create_content'),
    path('go/<str:redirect_id>/', redirect_view, name='redirect_view'),
    path('page/<slug:slug>/', custom_serve, name='inner_page'),
    path('', custom_serve),
    #path('<path:path>', custom_serve),
]