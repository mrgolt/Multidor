from django.urls import path
from .views import custom_serve

urlpatterns = [
    path('<path:path>', custom_serve),
]