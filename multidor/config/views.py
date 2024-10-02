from django.shortcuts import render
import os
from config.models import *
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpRequest
from urllib.parse import urlparse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import SitesSerializer, CasinoSerializer, BonusSerializer, ContentSerializer, ImageSerializer
import random
from django.shortcuts import HttpResponse
from django.db.models import Count, Sum
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
import requests
import time
import hashlib


def custom_serve(request, slug=None):
    domain = request.META.get('HTTP_HOST', '')
    parts = domain.split('.')

    # Если поддомен, ссылаемся на домен 2 уровня
    if len(parts) > 2 and domain != '127.0.0.1:8000':
        domain = '.'.join(parts[-2:])

    if domain == '127.0.0.1:8000':
        domain = 'aztec-gold.fun'

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
        bonuses = Bonus.objects.filter(is_active=True).order_by('sorting_order')
        content = Content.objects.filter(is_main=True, site=site)
        symbols = Symbol.objects.filter(is_active=True, website=site).order_by('sorting_order')
        images = Image.objects.filter(site=site)

        if site.type == 'casino':
            bonuses = Bonus.objects.filter(casino=site.casino).order_by('sorting_order')

        # Фильтрация контента на основе переданного slug
        if slug:
            content = Content.objects.filter(site=site, slug=slug)
        # Если нет такого контента на этом сайте, берем с другого, нужно для технических страниц
        if not content:
            content = Content.objects.filter(slug=slug)

        comments = Comment.objects.filter(page=content[0], created_at__lte=timezone.now()).order_by('-created_at')

        inner_pages = Content.objects.filter(is_main=False, site=site, is_popular=True)
        version_pages = Content.objects.filter(is_version_page=True, site=site)
        gambling_resources = GamblingResource.objects.filter(is_active=True)
        faqs = FAQ.objects.filter(content=content.first())
        accepted_answer = FAQ.objects.filter(content=content.first(), is_accepted=True).first()

    except Sites.DoesNotExist:
        site = None

    #template_path = os.path.join(domain, 'main.html')
    template_path = os.path.join('sweetbonanza.best', site.template_name)

    context = {
       'site': site,
       'bonuses': bonuses,
       'symbols': symbols,
       'content': content,
       'images': images,
       'inner_pages': inner_pages,
       'version_pages': version_pages,
       'random_classes': random_classes,
       'faqs': faqs,
       'accepted_answer': accepted_answer,
       'gambling_resources': gambling_resources,
       'comments': comments,
        'domain_hash': compute_hash(domain),
    }

    return render(request, template_path, context)

def redirect_view(request, redirect_id):

    redirect_type = 'CPA'

    domain = request.META.get('HTTP_HOST', '')
    yaid = request.GET.get('yaid')
    ymcounter = request.GET.get('ymcounter')

    parts = domain.split('.')

    if len(parts) > 2 and domain != '127.0.0.1:8000':
        domain = '.'.join(parts[-2:])

    if domain == '127.0.0.1:8000':
        domain = 'gatesofolympus.best'

    # Находим объект Sites по домену
    site = Sites.objects.get(allowed_domain=domain)

    redirect_obj = Redirect.objects.filter(name=redirect_id, site=site, type=redirect_type).first()

    if not redirect_obj:
        redirect_obj = Redirect.objects.filter(name=redirect_id, site=None, type=redirect_type).first()

    if not redirect_obj:
        redirect_obj = Redirect.objects.filter(name=redirect_id, type=redirect_type).first()

    click = Click.objects.create(redirect=redirect_obj, site=site, aff=redirect_obj.aff)

    # Увеличиваем счетчик кликов для объекта Redirect
    redirect_obj.increment_visits()

    url = redirect_obj.target_url
    if domain:
        url += '&domain=' + domain
    if yaid:
        url += '&yaid=' + yaid
    if ymcounter:
        url += '&ymcounter=' + ymcounter

    # Перенаправляем на целевой URL
    # return redirect(redirect_obj.target_url + '?click_id=' + str(click.id))
    return redirect(url)

def sitemap_generator(request):
    domain = request.META.get('HTTP_HOST', '')
    parts = domain.split('.')

    if len(parts) > 2 and domain != '127.0.0.1:8000':
        domain = '.'.join(parts[-2:])

    if domain == '127.0.0.1:8000':
        domain = 'gatesofolympus.best'

    try:
        site = Sites.objects.filter(allowed_domain=domain)[0]
        inner_pages = Content.objects.filter(is_main=False, site=site)
    except Sites.DoesNotExist:
        site = None

    template_path = os.path.join('sweetbonanza.best', 'sitemap.xml')

    return render(request, template_path, {'domain': domain, 'inner_pages': inner_pages})


def postbackcats_reg(request):
    campaign_id = request.GET.get('campaign_id')
    promo_id = request.GET.get('promo_id')
    visit_id = request.GET.get('visit_id')
    player_id = request.GET.get('player_id')
    click_id = request.GET.get('click_id')

    click = get_object_or_404(Click, id=click_id)

    if AffReg.objects.filter(player_id=player_id).exists():
        return HttpResponse("Player ID is already exists.")

    AffReg.objects.create(
        campaign_id=campaign_id,
        promo_id=promo_id,
        visit_id=visit_id,
        player_id=player_id,
        click=click,
        aff=click.aff,
    )
    return HttpResponse("Reg object created successfully.")

def postbackcats_dep(request):
    campaign_id = request.GET.get('campaign_id')
    promo_id = request.GET.get('promo_id')
    visit_id = request.GET.get('visit_id')
    player_id = request.GET.get('player_id')
    click_id = request.GET.get('click_id')
    amount = request.GET.get('amount')
    amount_cents = request.GET.get('amount_cents')
    currency = request.GET.get('currency')
    deposit_id = request.GET.get('deposit_id')

    click = get_object_or_404(Click, id=click_id)

    is_first = True

    if AffDep.objects.filter(deposit_id=deposit_id).exists():
        return HttpResponse("Dep ID is already exists.")

    if AffDep.objects.filter(player_id=player_id).exists():
        is_first = False

    AffDep.objects.create(
        campaign_id=campaign_id,
        promo_id=promo_id,
        visit_id=visit_id,
        player_id=player_id,
        amount=amount,
        amount_cents=amount_cents,
        currency=currency,
        click=click,
        aff=click.aff,
        is_first=is_first,
        deposit_id=deposit_id,
    )
    return HttpResponse("Dep object created successfully.")


def offlineconv(request):

    #https://www1.doghouseslot.online/#access_token=y0_AgAAAABn9W-5AAwcwwAAAAEKqUHyAABRiA25H0FJV7_7kShXd_cN4mqbow&token_type=bearer&expires_in=31536000&cid=95u42dc804yrdqy6yn7tcdftug

    #/offlineconv/?event_type=offline_reg&yaid=1712766804149415684&ymcounter=96162480

    event_type = request.GET.get('event_type')
    yaid = request.GET.get('yaid')
    ymcounter = request.GET.get('ymcounter')

    token = "y0_AgAAAABn9W-5AAwdRAAAAAEKrpCXAADPV940gX5BzLbS0CkKtBRtMu78Dw"

    file = f'ClientId,Target,DateTime\n{yaid},{event_type},{int(time.time())}'

    id_type = "CLIENT_ID"

    url = "https://api-metrika.yandex.net/management/v1/counter/{}/offline_conversions/upload?client_id_type={}".format(
        ymcounter, id_type)

    headers = {
        "Authorization": "OAuth {}".format(token)
    }

    res = requests.post(url, headers=headers, files={"file":file})

    return HttpResponse(res)






#@user_passes_test(lambda u: u.is_superuser)
def all_stats(request):
    template_path = os.path.join('sweetbonanza.best', 'all_stats.html')

    # Получение даты начала текущего месяца
    default_start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    date_clicked__gte = request.GET.get('date_clicked__gte', default_start_date)
    date_clicked__lte = request.GET.get('date_clicked__lte', '')

    # Получаем все сайты
    all_sites = Sites.objects.all()

    # Создаем пустые списки для хранения статистики
    site_stats = []

    # Проходимся по каждому сайту
    for site in all_sites:
        # Фильтрация кликов по дате
        clicks = Click.objects.filter(site=site)
        if date_clicked__gte:
            clicks = clicks.filter(date_clicked__gte=date_clicked__gte)
        if date_clicked__lte:
            clicks = clicks.filter(date_clicked__lte=date_clicked__lte)

        click_count = clicks.count()

        # Фильтрация регистраций по дате
        registrations = AffReg.objects.filter(click__site=site)
        if date_clicked__gte:
            registrations = registrations.filter(reg_date__gte=date_clicked__gte)
        if date_clicked__lte:
            registrations = registrations.filter(reg_date__lte=date_clicked__lte)

        registration_count = registrations.count()

        # Фильтрация депозитов по дате
        deposits = AffDep.objects.filter(click__site=site)
        if date_clicked__gte:
            deposits = deposits.filter(dep_date__gte=date_clicked__gte)
        if date_clicked__lte:
            deposits = deposits.filter(dep_date__lte=date_clicked__lte)

        deposit_count = deposits.count()

        fd = deposits.filter(is_first=True)
        fd_count = fd.count()

        # Агрегация суммы депозитов по дате
        deposit_sum = deposits.aggregate(total_amount=Sum('amount'))['total_amount']
        fd_sum = fd.aggregate(total_amount=Sum('amount'))['total_amount']

        # Создаем словарь с данными статистики для текущего сайта
        site_stat = {
            'name': site,
            'click_count': click_count,
            'registration_count': registration_count,
            'fd_count': fd_count,
            'deposit_count': deposit_count,
            'fd_sum': fd_sum,
            'deposit_sum': deposit_sum,
        }

        # Добавляем данные статистики в список
        if site_stat['click_count'] > 0 or site_stat['registration_count'] > 0 or site_stat['fd_count'] > 0 or site_stat['deposit_count'] > 0:
            site_stats.append(site_stat)

        site_stats = sorted(site_stats, key=lambda x: x['fd_count'], reverse=True)

    # Передаем данные в шаблон
    return render(request, template_path, {'site_stats': site_stats})

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

@api_view(['POST'])
def create_image(request):
    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_casinos(request):
    # Получаем все объекты Casino из базы данных
    casinos = Casino.objects.all()

    # Сериализуем данные
    serializer = CasinoSerializer(casinos, many=True)

    # Возвращаем сериализованные данные в ответе
    return Response(serializer.data)
@api_view(['GET'])
def get_images(request):
    # Получаем параметры запроса
    site_id = request.query_params.get('site', None)
    image_type = request.query_params.get('type', None)

    # Получаем все объекты Image из базы данных
    images = Image.objects.all()

    # Применяем фильтрацию, если параметры указаны
    if site_id is not None:
        images = images.filter(site=site_id)  # Фильтруем по ID сайта
    if image_type is not None:
        images = images.filter(type=image_type)  # Фильтруем по типу изображения

    # Сериализуем данные
    serializer = ImageSerializer(images, many=True)

    # Возвращаем сериализованные данные в ответе
    return Response(serializer.data)

@api_view(['GET'])
def get_contents(request):
    # Получаем параметры запроса
    site_id = request.query_params.get('site', None)
    slug = request.query_params.get('slug', None)

    # Получаем все объекты Image из базы данных
    items = Content.objects.all()

    # Применяем фильтрацию, если параметры указаны
    if site_id is not None:
        items = items.filter(site=site_id)  # Фильтруем по ID сайта
    if slug is not None:
        items = items.filter(slug=slug)  # Фильтруем по типу изображения

    # Сериализуем данные
    serializer = ContentSerializer(items, many=True)

    # Возвращаем сериализованные данные в ответе
    return Response(serializer.data)


@api_view(['GET'])
def get_casino_by_name(request, name):
    # Ищем казино по имени
    casinos = Casino.objects.filter(
        name__icontains=name)  # Используем icontains для нечувствительного к регистру поиска

    # Сериализуем данные
    serializer = CasinoSerializer(casinos, many=True)

    # Возвращаем сериализованные данные в ответе
    return Response(serializer.data)

@api_view(['GET'])
def get_site_by_name(request, name):
    # Ищем казино по имени
    sites = Sites.objects.filter(
        allowed_domain__icontains=name)  # Используем icontains для нечувствительного к регистру поиска

    # Сериализуем данные
    serializer = SitesSerializer(sites, many=True)

    # Возвращаем сериализованные данные в ответе
    return Response(serializer.data)


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

def compute_hash(domain_name):
    # Создаем объект хэширования
    hash_object = hashlib.md5()

    # Обновляем объект хэширования с доменным именем
    hash_object.update(domain_name.encode('utf-8'))

    # Получаем хэш в шестнадцатеричном формате
    hash_hex = hash_object.hexdigest()

    return hash_hex