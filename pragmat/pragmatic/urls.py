"""
URL configuration for pragmatic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from slots.views import SlotViewSet, page_detail
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'slots', SlotViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('slots/', include('slots.urls')),
    path('page/<slug:slug>/', page_detail, name='page_detail'),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)