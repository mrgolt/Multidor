from django.shortcuts import render
import os
from config.models import Sites, Bonus, Content, Casino, Redirect
from django.shortcuts import redirect, get_object_or_404


from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import SitesSerializer, CasinoSerializer, BonusSerializer, ContentSerializer


def custom_serve(request, slug=None):
    domain = request.META.get('HTTP_HOST', '')

    if domain == '127.0.0.1:8000':
        domain = 'sweetbonanza.best'

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
    template_path = os.path.join('sweetbonanza.best', 'main.html')

    return render(request, template_path, {'site': site, 'bonuses': bonuses, 'content': content, 'inner_pages': inner_pages})

def redirect_view(request, redirect_id):
    redirect_obj = get_object_or_404(Redirect, name=redirect_id)
    redirect_obj.increment_visits()
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