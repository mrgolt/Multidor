from django.shortcuts import render, get_object_or_404
from slots.models import Slot, SlotDescription
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Site, Offer
from django.utils import timezone
from datetime import timedelta
import requests
from django.http import HttpResponseBadRequest
import re
from django.utils.translation import get_language

def home(request):

    site = request.site

    template = site.home_template or 'home.html'

    first_offer = site.offers.first()

    home_page_slots = Slot.objects.filter(provider=site.provider).order_by('-id')[:48]
    popular_slots = Slot.objects.filter(is_popular=True, provider=site.provider, slot_type=1).order_by('-id')[:12]
    instant_win_games = Slot.objects.filter(provider=site.provider, slot_type=2).order_by('-id')[:12]
    scratch_cards = Slot.objects.filter(provider=site.provider, slot_type=3).order_by('-id')[:12]
    new_slots = Slot.objects.filter(provider=site.provider).order_by('-id')[:12]
    users_choice_slots = Slot.objects.filter(users_choice=True, provider=site.provider).order_by('-id')[:12]

    home_page_slots = update_slots_with_descriptions(site, home_page_slots)
    popular_slots = update_slots_with_descriptions(site, popular_slots)
    new_slots = update_slots_with_descriptions(site, new_slots)
    users_choice_slots = update_slots_with_descriptions(site, users_choice_slots)
    instant_win_games = update_slots_with_descriptions(site, instant_win_games)
    scratch_cards = update_slots_with_descriptions(site, scratch_cards)

    return render(request, template, {
        'home_page_slots': home_page_slots,
        'popular_slots': popular_slots,
        'new_slots': new_slots,
        'users_choice_slots': users_choice_slots,
        'instant_win_games': instant_win_games,
        'scratch_cards': scratch_cards,
        'offer': first_offer,
        'site': site,
    })

def promo_page(request):

    site = request.site

    template = site.home_template or 'home.html'

    home_page_slots = Slot.objects.filter(provider=site.provider).order_by('-id')[:48]
    popular_slots = Slot.objects.filter(is_popular=True, provider=site.provider, slot_type=1).order_by('-id')[:12]
    instant_win_games = Slot.objects.filter(provider=site.provider, slot_type=2).order_by('-id')[:12]
    scratch_cards = Slot.objects.filter(provider=site.provider, slot_type=3).order_by('-id')[:12]
    new_slots = Slot.objects.filter(provider=site.provider).order_by('-id')[:12]
    users_choice_slots = Slot.objects.filter(users_choice=True, provider=site.provider).order_by('-id')[:12]

    return render(request, template, {
        'home_page_slots': home_page_slots,
        'is_promo': True,
        'site': site,
        'users_choice_slots': users_choice_slots,
        'instant_win_games': instant_win_games,
        'scratch_cards': scratch_cards,
        'popular_slots': popular_slots,
        'new_slots': new_slots,
    })


def redirect_view(request, slug):

    site = request.site

    offers = site.offers.filter(redirect_name=slug)
    redirect_url = offers[0].redirect_url + '?placement=' + request.GET.get('placement') + '&offer=' + offers[0].redirect_name + '&domain=' + site.domain

    if request.GET.get('second_id'):
        redirect_url += '&second_id=' + request.GET.get('second_id')

    if redirect_url:
        return redirect(redirect_url)  # Выполняем редирект
    else:
        return redirect('default_view')  # Редирект на страницу по умолчанию, если slug не найден

def robots_txt(request):

    site = request.site

    lines = [
        "User-agent: *",
        "Disallow: /play/",
        f"sitemap: https://{site.domain}/sitemap.xml",
    ]
    response = HttpResponse("\n".join(lines), content_type="text/plain")
    response['Content-Disposition'] = 'inline; filename="robots.txt"'
    return response

def index_now(request, indexnow_key):
    return HttpResponse(indexnow_key)

def sitemap_generator(request):

    yesterday = (timezone.now().date() - timedelta(days=1)).strftime('%Y-%m-%d')

    site = request.site

    slots = Slot.objects.filter(provider=site.provider)

    # for slot in slots:
    #     print(requests.get(f'https://yandex.com/indexnow?key={slot.slug[0]}iyg786g8srfiIJHIuhiuhf7&url=https://{site.domain}/slots/{slot.slug}/').json())

    return render(request, 'sitemap.xml', {'domain': site.domain, 'yesterday': yesterday, 'slots': slots })

def yandex_webmaster_approve(request, code):

    user_agent = request.META.get('HTTP_USER_AGENT', '')
    if 'yandex' not in user_agent.lower():
        return HttpResponseBadRequest("Error")

    if not re.match("^[a-zA-Z0-9]+$", code):
        return HttpResponseBadRequest("Error")

    content = f"""
        <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            </head>
            <body>Verification: {code}</body>
        </html>
    """
    response = HttpResponse(content, content_type="text/plain")
    response['Content-Disposition'] = f'inline; filename="yandex_{code}.html"'
    return response


def endorphina_demo(request, game_symbol):
    response = requests.get(f'https://endorphina.com/games/{game_symbol}/play')
    return HttpResponse(response.content)

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def update_slots_with_descriptions(site, slots):
    current_language = get_language()
    for slot in slots:
        # Ищем объект SlotDescription для текущего слота и языка
        description_obj = SlotDescription.objects.filter(
            site=site, slot=slot, language__code=current_language
        ).first()

        # Обновляем слот с описанием и сниппетом, если они есть
        slot.description = description_obj.description if description_obj else slot.description
        slot.snippet = description_obj.snippet if description_obj else slot.snippet

    return slots