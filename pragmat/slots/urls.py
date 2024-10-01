from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SlotViewSet, slot_list, slot_detail



urlpatterns = [
    path('', slot_list, name='slot_list'),
    path('<slug:slug>/', slot_detail, name='slot_detail'),
]