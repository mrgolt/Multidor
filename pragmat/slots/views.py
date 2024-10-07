from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import SlotSerializer
from rest_framework import viewsets
from django.core.paginator import Paginator
from django.db.models import Q
from pragmatic.views import get_site
from rest_framework.response import Response
from rest_framework import status
import requests

def slot_list(request):

    site = get_site(request)

    slot_name = request.GET.get('slot_name')
    page_number = request.GET.get('page', 1)  # Получаем номер страницы из параметров запроса
    slot_type = request.GET.get('slot_type')

    slot_type = SlotType.objects.filter(id=slot_type).first()

    keywords_mapping = {
        'Сладости и Фрукты': ['sugar', 'sweet', 'фрукт', 'сладк'],
        'Дикий запад': ['cowboys', 'ковбои', 'wild west', 'дикий запад'],
    }

    slots = Slot.objects.filter(provider=site.provider).order_by('-sorting_order')

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

    # Параметры пагинации
    slots_per_page = 18
    paginator = Paginator(slots, slots_per_page)  # Создаём объект Paginator
    page_obj = paginator.get_page(page_number)  # Получаем текущую страницу

    popular_slots = Slot.objects.filter(is_popular=True, provider=site.provider).order_by('-id')[:10]
    new_slots = Slot.objects.filter(is_new=True, provider=site.provider).order_by('-id')[:10]
    users_choice_slots = Slot.objects.filter(users_choice=True, provider=site.provider).order_by('-id')[:10]

    context = {
        'slots': page_obj,  # Передаём объект страницы в контекст
        'popular_slots': popular_slots,
        'new_slots': new_slots,
        'users_choice_slots': users_choice_slots,
        'slot_name': slot_name,
        'site': site,
        'slot_type': slot_type,
    }

    return render(request, site.slot_list_template, context)


def slot_detail(request, slug):

    site = get_site(request)

    slot = get_object_or_404(Slot, slug=slug, provider=site.provider)
    reviews = Review.objects.filter(slot=slot)[:10]
    popular_slots = Slot.objects.filter(is_popular=True, provider=site.provider, slot_type=slot.slot_type).order_by('-id')[:10]
    new_slots = Slot.objects.filter(is_new=True, provider=site.provider, slot_type=slot.slot_type).order_by('-id')[:10]
    users_choice_slots = Slot.objects.filter(users_choice=True, provider=site.provider, slot_type=slot.slot_type).order_by('-id')[:10]

    if slot.provider.id == 2:
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15',
        ]

        headers = {'User-Agent': user_agents[0]}

        response = requests.get(f"https://static-live.hacksawgaming.com/{slot.game_symbol}/version.json", headers=headers)

        if response.status_code == 200:
            data = response.json()
            version = data.get("version")
            slot.version = version
            slot.save()

    return render(request, site.slot_detail_template, {'site': site, 'slot': slot, 'reviews': reviews, 'popular_slots': popular_slots, 'new_slots': new_slots, 'users_choice_slots': users_choice_slots})

class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

    def dispatch(self, request, *args, **kwargs):
        api_key = request.POST.get('api_key')  # Получаем api_key из параметров запроса
        if api_key != 'aB3dE5fG7hJ8kL9mN0pQ1rS2tU3vW4xYz':
            return Response({'detail': 'Invalid API key'}, status=status.HTTP_403_FORBIDDEN)
        return super().dispatch(request, *args, **kwargs)

def page_detail(request, slug):

    site = get_site(request)

    page = get_object_or_404(Page, slug=slug)
    popular_slots = Slot.objects.filter(is_popular=True, provider=site.provider)[:10]
    new_slots = Slot.objects.filter(is_new=True, provider=site.provider)[:10]
    users_choice_slots = Slot.objects.filter(users_choice=True, provider=site.provider)[:10]

    return render(request, site.page_detail_template, {'site': site, 'page': page, 'popular_slots': popular_slots, 'new_slots': new_slots, 'users_choice_slots': users_choice_slots})