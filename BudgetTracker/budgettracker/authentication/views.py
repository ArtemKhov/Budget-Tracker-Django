from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site

import json
from validate_email import validate_email

from authentication.utils import token_generator


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
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html',
                                  context={'title': 'Registration', 'fieldValues': request.POST})
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('auth:activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
                activate_url = f'http://{domain}{link}'

                email_subject = 'Activate your account'
                email_body = (f'Hi {user.username}. Please use this link to verify your account\n'
                              f'{activate_url}')
                email = EmailMessage(
                    email_subject,
                    email_body,
                    "noreply@semycolon.com",
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account successfully created.')
                return render(request, 'authentication/register.html',
                              context={'title': 'Registration'})

        return render(request, 'authentication/register.html',
                      context={'title': 'Registration'})

class VerificationView(View):
    def get(self, request, uidb64, token):
        return redirect('auth:login')