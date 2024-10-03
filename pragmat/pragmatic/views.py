from django.shortcuts import render
from slots.models import *
from django.shortcuts import redirect
from django.http import HttpResponse

REDIRECTS = {
    'kometa': 'https://stars-flight.com/sbcb5e2ca',
}

def home(request):
    popular_slots = Slot.objects.filter(is_popular=True).order_by('-id')[:10]
    new_slots = Slot.objects.filter(is_new=True).order_by('-id')[:10]
    users_choice_slots = Slot.objects.filter(users_choice=True).order_by('-id')[:10]
    reviews = Review.objects.all()[:10]

    return render(request, 'home.html', {'popular_slots': popular_slots, 'new_slots': new_slots, 'reviews': reviews, 'users_choice_slots': users_choice_slots})


def redirect_view(request, slug):
    # Получаем URL для редиректа по slug
    redirect_url = REDIRECTS.get(slug)

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