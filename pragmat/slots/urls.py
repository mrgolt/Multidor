from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SlotViewSet, slot_list, slot_detail, optimized_logo



urlpatterns = [
    path('', slot_list, name='slot_list'),
    path('optimized_logo/<slug:slug>/', optimized_logo, name='optimized_logo'),
    path('<slug:slug>/', slot_detail, name='slot_detail'),
]