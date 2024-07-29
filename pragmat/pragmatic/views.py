from django.shortcuts import render
from slots.models import *


def home(request):
    popular_slots = Slot.objects.filter(is_popular=True)[:10]
    new_slots = Slot.objects.filter(is_new=True)[:10]
    users_choice_slots = Slot.objects.filter(users_choice=True)[:10]
    reviews = Review.objects.all()[:10]

    return render(request, 'home.html', {'popular_slots': popular_slots, 'new_slots': new_slots, 'reviews': reviews, 'users_choice_slots': users_choice_slots})