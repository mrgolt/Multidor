from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import SlotSerializer, SlotDescriptionSerializer
from rest_framework import viewsets
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
import requests
from django.utils import timezone
from datetime import timedelta
from pragmatic.views import update_slots_with_descriptions
from django.utils.translation import get_language
from django.db.models import Case, When
from django.views.decorators.cache import cache_page
import random

@cache_page(60 * 60 * 24)
def slot_list(request):

    site = request.site

    slot_name = request.GET.get('slot_name')
    page_number = request.GET.get('page', 1)
    slot_type = request.GET.get('slot_type')
    theme_id = request.GET.get('theme')
    feature = request.GET.get('feature')
    payline = request.GET.get('payline')

    slot_type = SlotType.objects.filter(id=slot_type).first()

    theme = None

    if theme_id:
        theme = get_object_or_404(Theme, id=theme_id)

    keywords_mapping = {
        'Сладости и Фрукты': ['sugar', 'sweet', 'фрукт', 'сладк'],
        'Дикий запад': ['cowboys', 'ковбои', 'wild west', 'дикий запад'],
    }

    slots = Slot.objects.filter(provider=site.provider).order_by('-id')

    if slot_name:

        if slot_name in keywords_mapping:
            keywords = keywords_mapping[slot_name]
            q_objects = Q()
            for keyword in keywords:
                q_objects |= Q(description__icontains=keyword)

            slots = slots.filter(q_objects)
        else:
            slots = slots.filter(
                Q(name__icontains=slot_name) | Q(folk_name__icontains=slot_name) | Q(description__icontains=slot_name))

    if slot_type:
        slots = slots.filter(slot_type=slot_type)
    if theme:
        slots = slots.filter(theme=theme)
    if feature:
        feature_object = Feature.objects.get(id=feature)
        if feature_object:
            slots = slots.filter(features=feature_object)
    if payline:
        slots = slots.filter(paylines=payline)

    # Параметры пагинации
    slots_per_page = 18
    paginator = Paginator(slots, slots_per_page)  # Создаём объект Paginator
    page_obj = paginator.get_page(page_number)  # Получаем текущую страницу

    popular_slots = Slot.objects.filter(is_popular=True, provider=site.provider).order_by('-id')[:10]
    new_slots = Slot.objects.filter(provider=site.provider).order_by('-id')[:10]
    users_choice_slots = Slot.objects.filter(users_choice=True, provider=site.provider).order_by('-id')[:10]

    popular_slots = update_slots_with_descriptions(site, popular_slots)
    page_obj = update_slots_with_descriptions(site, page_obj)

    context = {
        'slots': page_obj,  # Передаём объект страницы в контекст
        'popular_slots': popular_slots,
        'new_slots': new_slots,
        'users_choice_slots': users_choice_slots,
        'slot_name': slot_name,
        'site': site,
        'slot_type': slot_type,
        'theme': theme,
        'feature': feature,
        'payline': payline,
    }

    return render(request, site.slot_list_template, context)

@cache_page(60 * 60 * 24)
def slot_detail(request, slug):

    site = request.site

    current_language = get_language()

    slot = get_object_or_404(Slot, slug=slug, provider=site.provider)
    reviews = Review.objects.filter(slot=slot)[:10]
    popular_slots = Slot.objects.filter(is_popular=True, provider=site.provider, slot_type=slot.slot_type).order_by('-id')[:10]
    new_slots = Slot.objects.filter(provider=site.provider, slot_type=slot.slot_type).order_by('-id')[:10]
    users_choice_slots = Slot.objects.filter(users_choice=True, provider=site.provider, slot_type=slot.slot_type).order_by('-id')[:10]

    popular_slots = update_slots_with_descriptions(site, popular_slots)

    if slot.similar_slots:
        similar_slots = Slot.objects.filter(id__in=slot.similar_slots, provider=site.provider).annotate(
            order=Case(
                *[When(id=slot_id, then=idx) for idx, slot_id in enumerate(slot.similar_slots)],
                default=len(slot.similar_slots)  # Если не найдено, ставим в конец
            )
        ).order_by('order')
    else:
        similar_slots = []

    is_mobile = request.user_agent.is_mobile

    slot_description = SlotDescription.objects.filter(
            site=site, slot=slot, language__code=current_language
        ).first()

    if slot_description:
        slot.description = slot_description.description
        slot.snippet = slot_description.snippet

    # Проверяем, если провайдер Hacksaw
    if slot.provider.id == 2:
        # Проверяем, прошло ли больше 3 дней с момента последнего обновления
        if timezone.now() - slot.updated_at > timedelta(days=7):
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15',
            ]

            headers = {'User-Agent': user_agents[0]}

            response = requests.get(f"https://static-live.hacksawgaming.com/{slot.game_symbol}/version.json",
                                    headers=headers)

            if response.status_code == 200:
                data = response.json()
                version = data.get("version")
                slot.version = version
                slot.save()

    return render(request, site.slot_detail_template, {
        'site': site,
        'slot': slot,
        'reviews': reviews,
        'popular_slots': popular_slots,
        'new_slots': new_slots,
        'users_choice_slots': users_choice_slots,
        'is_mobile': is_mobile,
        'current_language': current_language,
        'similar_slots': similar_slots,
    })

class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

    def get_queryset(self):
        provider_id = self.request.query_params.get('provider_id', None)
        if provider_id is not None:
            return self.queryset.filter(provider_id=provider_id)
        return self.queryset

    def list(self, request, *args, **kwargs):
        api_key = request.GET.get('api_key') or request.POST.get('api_key')
        if api_key != 'aB3dE5fG7hJ8kL9mN0pQ1rS2tU3vW4xYz':
            return Response({'detail': 'Invalid API key'}, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)

class SlotDescriptionsViewSet(viewsets.ModelViewSet):
    queryset = SlotDescription.objects.all()
    serializer_class = SlotDescriptionSerializer

    def dispatch(self, request, *args, **kwargs):
        api_key = request.POST.get('api_key')  # Получаем api_key из параметров запроса
        if api_key != 'aB3dE5fG7hJ8kL9mN0pQ1rS2tU3vW4xYz':
            return Response({'detail': 'Invalid API key'}, status=status.HTTP_403_FORBIDDEN)
        return super().dispatch(request, *args, **kwargs)

@cache_page(60 * 60 * 24)
def page_detail(request, slug):

    site = request.site

    page = get_object_or_404(Page, slug=slug)
    popular_slots = Slot.objects.filter(is_popular=True, provider=site.provider)[:10]
    new_slots = Slot.objects.filter(provider=site.provider)[:10]
    users_choice_slots = Slot.objects.filter(users_choice=True, provider=site.provider)[:10]

    return render(request, site.page_detail_template, {'site': site, 'page': page, 'popular_slots': popular_slots, 'new_slots': new_slots, 'users_choice_slots': users_choice_slots})


@cache_page(60 * 60 * 24 * 30)
def optimized_logo(request, slug):
    site = request.site
    slot = get_object_or_404(Slot, slug=slug, provider=site.provider)

    # Получаем логотип слота
    logo = slot.logo

    # Открываем изображение с помощью Pillow
    image = Image.open(logo)

    # Генерируем случайное качество от 65 до 75
    quality = random.randint(65, 75)

    # Создаем объект BytesIO для хранения изображения в памяти
    img_byte_arr = io.BytesIO()

    # Сохраняем изображение в формате WebP
    image.save(img_byte_arr, format='WEBP', quality=quality)
    img_byte_arr.seek(0)

    # Возвращаем изображение в ответе
    return HttpResponse(img_byte_arr, content_type='image/webp')