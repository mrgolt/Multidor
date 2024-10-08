from django.shortcuts import render, get_object_or_404
from slots.models import *
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Site, Offer

def get_site(request):
    # Получаем хост из запроса
    domain = request.META['HTTP_HOST']

    if domain == '127.0.0.1:8000':
        domain = 'pragmatic-play.cloud'
    else:
        domain = '.'.join(domain.split('.')[-2:])

    site = get_object_or_404(Site, domain=domain)

    return site

def home(request):

    site = get_site(request)

    template = site.home_template or 'home.html'

    first_offer = site.offers.first()

    popular_slots = Slot.objects.filter(is_popular=True, provider=site.provider, slot_type=1).order_by('-id')[:12]
    instant_win_games = Slot.objects.filter(provider=site.provider, slot_type=2).order_by('-id')[:12]
    scratch_cards = Slot.objects.filter(provider=site.provider, slot_type=3).order_by('-id')[:12]
    new_slots = Slot.objects.filter(is_new=True, provider=site.provider).order_by('-id')[:12]
    users_choice_slots = Slot.objects.filter(users_choice=True, provider=site.provider).order_by('-id')[:12]
    reviews = Review.objects.all()[:10]

    return render(request, template, {
        'popular_slots': popular_slots,
        'new_slots': new_slots,
        'reviews': reviews,
        'users_choice_slots': users_choice_slots,
        'instant_win_games': instant_win_games,
        'scratch_cards': scratch_cards,
        'offer': first_offer,
        'site': site,
    })


def redirect_view(request, slug):
    # Получаем URL для редиректа по slug

    site = get_site(request)

    offers = site.offers.filter(redirect_name=slug)
    redirect_url = offers[0].redirect_url + '?placement=' + request.GET.get('placement') + '&offer=' + offers[0].redirect_name + '&domain=' + site.domain

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

def index_now(request, indexnow_key):
    return HttpResponse(indexnow_key)