from django.shortcuts import render
import os
from config.models import *
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpRequest
from urllib.parse import urlparse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import SitesSerializer, CasinoSerializer, BonusSerializer, ContentSerializer
import random


def custom_serve(request, slug=None):
    domain = request.META.get('HTTP_HOST', '')

    if domain == '127.0.0.1:8000':
        domain = 'volcano-riches.fun'

    classes = [
        'has-game-preview',
        'is-valid-game-amount',
        'has-provider-dark',
        'is-valid-slot',
        'has-game-preview-provider',
        'is-valid-game-amount-review',
        'has-provider-dark-game',
        'is-active-widget-service',
        'has-dark-theme-provider',
        'is-responsive-layout-author',
        'has-hidden-sidebar-game',
        'is-expanded-menu-service',
        'has-overlay-background-review',
        'is-animated-button-provider',
        'has-game-overlay-service',
        'is-valid-provider-widget',
        'has-review-carousel-game',
        'is-service-popup-author',
        'has-dark-mode-toggle-provider',
        'is-author-bio-service',
        'has-game-stats-review',
        'is-provider-dropdown-game',
        'has-service-loader-author',
        'is-review-panel-provider',
        'has-service-dropdown-game',
        'is-provider-modal-review',
        'has-game-loader-provider',
        'is-dark-theme-toggle-service',
        'has-author-overlay-game',
        'is-valid-review-widget',
        'has-game-info-provider',
        'is-service-header-author',
        'has-dark-mode-toggle-game',
        'is-provider-popup-service',
        'has-review-carousel-provider',
        'is-active-game-panel-author',
        'has-service-dropdown-provider',
        'is-provider-modal-game',
        'has-dark-theme-toggle-review',
        'is-game-info-service',
        'has-author-overlay-review',
        'is-valid-service-widget',
        'has-game-loader-author',
        'is-dark-mode-toggle-provider',
        'has-provider-header-game',
        'is-review-carousel-service',
        'has-service-dropdown-review',
        'is-provider-modal-author',
        'has-dark-theme-toggle-game',
        'is-game-info-provider',
        'has-author-overlay-review',
        'is-valid-service-widget',
        'has-game-loader-author',
        'is-dark-mode-toggle-provider'
    ]

    random_classes_1 = [class_name for class_name in classes if domain[0] in class_name]
    random_classes_2 = [class_name for class_name in classes if domain[1] in class_name]
    random_classes_3 = [class_name for class_name in classes if domain[2] in class_name]
    random_classes = set(random_classes_1[:2] + random_classes_2[:2] + random_classes_3[:2])

    try:
        site = Sites.objects.filter(allowed_domain=domain)[0]
        bonuses = Bonus.objects.filter(is_active=True)
        content = Content.objects.filter(is_main=True, site=site)

        # Фильтрация контента на основе переданного slug
        if slug:
            content = Content.objects.filter(site=site, slug=slug)


        inner_pages = Content.objects.filter(is_main=False, site=site)

    except Sites.DoesNotExist:
        site = None

    #template_path = os.path.join(domain, 'main.html')
    template_path = os.path.join('sweetbonanza.best', site.template_name)

    return render(request, template_path, {'site': site, 'bonuses': bonuses, 'content': content, 'inner_pages': inner_pages, 'random_classes': random_classes})

def redirect_view(request, redirect_id):

    redirect_obj = get_object_or_404(Redirect, name=redirect_id)

    domain = request.META.get('HTTP_HOST', '')

    if domain == '127.0.0.1:8000':
        domain = 'voodooendorphina.fun'

    # Находим объект Sites по домену
    site = Sites.objects.get(allowed_domain=domain)

    Click.objects.create(redirect=redirect_obj, site=site)

    # Увеличиваем счетчик кликов для объекта Redirect
    redirect_obj.increment_visits()

    # Перенаправляем на целевой URL
    return redirect(redirect_obj.target_url)

@api_view(['POST'])
def create_site(request):
    serializer = SitesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_casino(request):
    serializer = CasinoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_bonus(request):
    serializer = BonusSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_content(request):
    serializer = ContentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_sites(request):
    # Получаем все объекты Sites из базы данных
    sites = Sites.objects.all()

    # Создаем пустой список для хранения данных о сайтах
    sites_data = []

    # Итерируемся по каждому сайту
    for site in sites:
        # Получаем количество связанных объектов Content для текущего сайта
        num_content = Content.objects.filter(site=site).count()

        # Сериализуем данные о сайте
        site_serializer = SitesSerializer(site)

        # Добавляем количество контента к данным о сайте
        site_data = site_serializer.data
        site_data['num_content'] = num_content

        # Добавляем данные о сайте в список
        sites_data.append(site_data)

    # Возвращаем ответ с данными и статусом HTTP 200 OK
    return Response(sites_data)


@api_view(['PUT'])
def update_site(request, site_id):
    try:
        site = Sites.objects.get(site_id=site_id)
    except Sites.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = SitesSerializer(site, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_site_field(request, site_id):
    try:
        site = Sites.objects.get(site_id=site_id)
    except Sites.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    field_name = request.data.get('field_name')
    field_value = request.data.get('field_value')

    if not field_name or not field_value:
        return Response({'error': 'Both field_name and field_value must be provided'}, status=status.HTTP_400_BAD_REQUEST)

    if field_name == 'site_id':
        return Response({'error': 'Cannot update site_id'}, status=status.HTTP_400_BAD_REQUEST)

    setattr(site, field_name, field_value)
    site.save()

    return Response({'message': f'Field {field_name} updated successfully'}, status=status.HTTP_200_OK)