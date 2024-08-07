from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import SlotSerializer
from rest_framework import viewsets
from django.core.paginator import Paginator
from django.db.models import Q

def slot_list(request):
    slot_name = request.GET.get('slot_name')
    page_number = request.GET.get('page', 1)  # Получаем номер страницы из параметров запроса

    keywords_mapping = {
        'Сладости и Фрукты': ['sugar', 'sweet', 'фрукт', 'сладк'],
        'Дикий запад': ['cowboys', 'ковбои', 'wild west', 'дикий запад'],

    }

    if slot_name:

        if slot_name in keywords_mapping:
            keywords = keywords_mapping[slot_name]
            q_objects = Q()
            for keyword in keywords:
                q_objects |= Q(description__icontains=keyword)

            slots = Slot.objects.filter(q_objects)
        else:
            slots = Slot.objects.filter(
                Q(name__icontains=slot_name) | Q(folk_name__icontains=slot_name) | Q(description__icontains=slot_name))

    else:
        slots = Slot.objects.all()

    # Параметры пагинации
    slots_per_page = 18
    paginator = Paginator(slots, slots_per_page)  # Создаём объект Paginator
    page_obj = paginator.get_page(page_number)  # Получаем текущую страницу

    popular_slots = Slot.objects.filter(is_popular=True)[:10]
    new_slots = Slot.objects.filter(is_new=True)[:10]
    users_choice_slots = Slot.objects.filter(users_choice=True)[:10]

    context = {
        'slots': page_obj,  # Передаём объект страницы в контекст
        'popular_slots': popular_slots,
        'new_slots': new_slots,
        'users_choice_slots': users_choice_slots,
        'slot_name': slot_name
    }

    return render(request, 'slot_list.html', context)


def slot_detail(request, slug):
    slot = get_object_or_404(Slot, slug=slug)
    reviews = Review.objects.filter(slot=slot)[:10]
    popular_slots = Slot.objects.filter(is_popular=True)[:10]
    new_slots = Slot.objects.filter(is_new=True)[:10]
    users_choice_slots = Slot.objects.filter(users_choice=True)[:10]

    return render(request, 'slot_detail.html', {'slot': slot, 'reviews': reviews, 'popular_slots': popular_slots, 'new_slots': new_slots, 'users_choice_slots': users_choice_slots})

class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    popular_slots = Slot.objects.filter(is_popular=True)[:10]
    new_slots = Slot.objects.filter(is_new=True)[:10]
    users_choice_slots = Slot.objects.filter(users_choice=True)[:10]

    return render(request, 'page_detail.html', {'page': page, 'popular_slots': popular_slots, 'new_slots': new_slots, 'users_choice_slots': users_choice_slots})