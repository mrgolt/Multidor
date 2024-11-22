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
from slots.views import SlotViewSet, SlotDescriptionsViewSet, page_detail
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

router = DefaultRouter()
router.register(r'slots', SlotViewSet)
router.register(r'slotdescriptions', SlotDescriptionsViewSet)

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path(_(''), views.home, name='home'),
    path(_('slots/'), include('slots.urls')),
    path(_('page/<slug:slug>/'), page_detail, name='page_detail'),
    path('api/', include(router.urls)),
    path('play/<slug:slug>/', views.redirect_view, name='redirect_view'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('promo/', views.promo_page, name='promo_page'),
    path(_('sitemap.xml'), views.sitemap_generator, name='sitemap_generator'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('get_proxy/', views.get_proxy, name='get_proxy'),
    path('get_key/', views.get_key, name='get_key'),
    path('get_site/', views.get_site, name='get_site'),
    path('<str:indexnow_key>.txt', views.index_now, name='index_now'),
    path('index_now/', views.send_index_now, name='send_index_now'),
    path('yandex_<str:code>.html', views.yandex_webmaster_approve, name='yandex_webmaster_approve'),
    path('endorphina-demo/<str:game_symbol>/', views.endorphina_demo, name='endorphina_demo'),
    path('pragmatic-play-demo/<path:path>', views.pragmatic_play_demo, name='pragmatic_play_demo'),
    prefix_default_language=False,
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'pragmatic.views.custom_404_view'