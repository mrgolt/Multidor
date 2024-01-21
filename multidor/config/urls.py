from django.urls import path
from .views import custom_serve

urlpatterns = [
    path('', custom_serve),
    path('<path:path>', custom_serve),
]