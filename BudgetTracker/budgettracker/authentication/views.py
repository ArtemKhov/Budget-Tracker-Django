from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages

import json
from validate_email import validate_email


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'},
                                status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry, username already using, choose another one'},
                                status=409)
        return JsonResponse({'username_valid': True})

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email not valid'},
                                status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry, email already using, choose another one'},
                                status=409)
        return JsonResponse({'email_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html',
                      context={'title': 'Registration'})

    def post(self, request):
        messages.success(request,'Success')
        messages.warning(request,'Warning')
        messages.info(request,'Info')
        messages.error(request,'Error')

        return render(request, 'authentication/register.html',
                      context={'title': 'Registration'})

