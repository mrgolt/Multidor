from django.shortcuts import render, get_object_or_404
from slots.models import *
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Site, Offer

def get_site(request):
    # Получаем хост из запроса
    domain_parts = request.META['HTTP_HOST'].split('.')

    # Проверяем, что домен содержит как минимум два элемента (например, 'pragmatic-play.cloud')
    if len(domain_parts) >= 2:
        # Берем последние два элемента (например, ['pragmatic-play', 'cloud'])
        second_level_domain = '.'.join(domain_parts[-2:])
    else:
        # Если домен некорректный, возвращаем его как есть (на всякий случай)
        second_level_domain = request.META['HTTP_HOST']

    if second_level_domain == '127.0.0.1:8000':
        second_level_domain = 'pragmatic-play.cloud'

    site = get_object_or_404(Site, domain='pragmatic-play.cloud')

    return site

def home(request):

    site = get_site(request)

    template = site.home_template or 'home.html'

    first_offer = site.offers.first()

    popular_slots = Slot.objects.filter(is_popular=True).order_by('-id')[:10]
    new_slots = Slot.objects.filter(is_new=True).order_by('-id')[:10]
    users_choice_slots = Slot.objects.filter(users_choice=True).order_by('-id')[:10]
    reviews = Review.objects.all()[:10]

    return render(request, template, {
        'popular_slots': popular_slots,
        'new_slots': new_slots,
        'reviews': reviews,
        'users_choice_slots': users_choice_slots,
        'offer': first_offer,
    })


def redirect_view(request, slug):
    # Получаем URL для редиректа по slug

    site = get_site(request)

    offers = site.offers.filter(redirect_name=slug)
    redirect_url = offers[0].redirect_url

    if redirect_url:
        return redirect(redirect_url)  # Выполняем редирект
    else:
        return redirect('default_view')  # Редирект на страницу по умолчанию, если slug не найден

def robots_txt(request):
    # Содержимое файла robots.txt
    lines = [
        "User-agent: *",
        "Disallow: /play/",
    ]
    response = HttpResponse("\n".join(lines), content_type="text/plain")
    response['Content-Disposition'] = 'inline; filename="robots.txt"'
    return response