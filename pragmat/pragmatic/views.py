from django.shortcuts import render, get_object_or_404
from slots.models import Slot, SlotDescription
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Site, Offer, FAQ
from django.utils import timezone
from datetime import timedelta
import requests
from django.http import HttpResponseBadRequest
import re
from django.utils.translation import get_language
import random
from django.views.decorators.cache import cache_page

@cache_page(60 * 60 * 24)
def home(request):

    site = request.site
    current_language = get_language()

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

    faqs = FAQ.objects.filter(provider=site.provider, language__code=current_language)

    return render(request, template, {
        'home_page_slots': home_page_slots,
        'popular_slots': popular_slots,
        'new_slots': new_slots,
        'users_choice_slots': users_choice_slots,
        'instant_win_games': instant_win_games,
        'scratch_cards': scratch_cards,
        'offer': first_offer,
        'site': site,
        'faqs': faqs,
    })

@cache_page(60 * 60 * 24)
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

@cache_page(60 * 60 * 24)
def robots_txt(request):

    site = request.site

    lines = [
        "User-agent: *",
        "Disallow: /play/",
        "Disallow: /static/assets/js/",
        f"sitemap: https://{site.domain}/sitemap.xml",
        f"sitemap: https://{site.domain}/es/sitemap.xml",
        f"sitemap: https://{site.domain}/en/sitemap.xml",
        f"sitemap: https://{site.domain}/pt/sitemap.xml",
        f"sitemap: https://{site.domain}/de/sitemap.xml",
    ]
    response = HttpResponse("\n".join(lines), content_type="text/plain")
    response['Content-Disposition'] = 'inline; filename="robots.txt"'
    return response

def index_now(request, indexnow_key):
    return HttpResponse(indexnow_key)

def sitemap_generator(request):

    current_language = get_language()
    if current_language == 'ru':
        lang_src = ''
    else:
        lang_src = current_language + '/'

    yesterday = (timezone.now().date() - timedelta(days=1)).strftime('%Y-%m-%d')

    site = request.site

    slots = Slot.objects.filter(provider=site.provider)

    # for slot in slots:
    #     print(requests.get(f'https://yandex.com/indexnow?key={slot.slug[0]}iyg786g8srfiIJHIuhiuhf7&url=https://{site.domain}/slots/{slot.slug}/').json())

    return render(request, 'sitemap.xml', {'domain': site.domain, 'yesterday': yesterday, 'slots': slots, 'lang_src': lang_src })

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
    site = request.site
    return render(request, site.notfound_template, {'site': site}, status=404)

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

def get_proxy(request):
    response = requests.get(f'http://178.253.40.210/proxy/get_stab_proxy.php?user=seo_dev1&pass=3GdBJ3DBsyu76&pid={random.randint(1000, 1000000)}')
    return HttpResponse(response.content)

def get_site(request):
    response = requests.get('https://infinitysoftcombine-v3.ru/task/get_site_ipv6.php?password=5b5ed5cdc7a466abd74836a514537a53&cat_string=', verify=False)
    return HttpResponse(response.content)

def get_key(request):
    response = requests.get(
        'https://redirect.processfinger.com/task/redirect.php?password=YBmGTrgo&server=1&yandex=1&ya_word_mode=1')

    content = response.content.decode('utf-8')

    start_tag = '<parse>'
    end_tag = '</parse>'

    start_index = content.find(start_tag) + len(start_tag)
    end_index = content.find(end_tag, start_index)

    if start_index != -1 and end_index != -1:
        parse_content = content[start_index:end_index]
    else:
        parse_content = 'Нет данных'

    return HttpResponse(parse_content)