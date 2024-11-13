from django.contrib import messages
from django.shortcuts import render

from utils import data_mixin
from .models import UserPreference


def index(request):
    context = data_mixin.extra_context
    context['title'] = 'Preferred Currency'

    is_user_exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None

    if is_user_exists:
        user_preferences = UserPreference.objects.get(user=request.user)
    if request.method == 'GET':
        context['user_preferences'] = user_preferences
        return render(request, 'userpreferences/index.html', context=context)

    if request.method == 'POST':
        currency = request.POST['currency']
        if is_user_exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved')
        context['user_preferences'] = user_preferences
        return render(request, 'userpreferences/index.html', context=context)


