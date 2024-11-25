from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator

import json
from validate_email import validate_email
import threading

from authentication.utils import token_generator
from utils import DataMixin

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)

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
                email_body = (f'Hi {user.username}. Please use this link to verify your account:\n'
                              f'{activate_url}')
                email = EmailMessage(
                    email_subject,
                    email_body,
                    "noreply@semycolon.com",
                    [email],
                )
                EmailThread(email).start()
                messages.success(request, 'Account successfully created. Please, check you Email to verify your account.')
                return render(request, 'authentication/register.html',
                              context={'title': 'Registration'})

        return render(request, 'authentication/register.html',
                      context={'title': 'Registration'})

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully!')
            return redirect('auth:login')
        elif not token_generator.check_token(user, token):
            messages.warning(request, 'User already activated')
            return redirect('auth:login')
        elif user.is_active:
            return redirect('auth:login')
        else:
            messages.error(request, 'Activation link is invalid!')
            return redirect('auth:login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f'Logged in {user.username} successfully.')
                    return redirect('home')
                messages.error(request, 'Account is not active, please check your Email.')
                return render(request, 'authentication/login.html')
            else:
                messages.error(request, 'Invalid credentials. Check your username/password and try again.')
                return render(request, 'authentication/login.html')
        messages.error(request, 'Please fill in all fields.')
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.warning(request, 'You have been logged out')
        return redirect('auth:login')

class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset_password.html')

    def post(self, request):
        email = request.POST['email']

        context = {
            'values': request.POST,
        }

        if not validate_email(email):
            messages.error(request, 'Please, supply a valid email')
            return render(request, 'authentication/reset_password.html', context)

        current_site = get_current_site(request)
        user = User.objects.filter(email=email)

        if user.exists():
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            }

            link = reverse('auth:reset-user-password', kwargs={
                'uidb64': email_contents['uid'], 'token': email_contents['token']})

            email_subject = 'Password reset'

            reset_url = 'http://' + current_site.domain + link

            email = EmailMessage(
                email_subject,
                'Hi! Please click the link below to reset your password \n' + reset_url,
                'noreply@semycolon.com',
                [email],
            )
            EmailThread(email).start()

        messages.success(request, 'Message was sent to your email to reset your password')
        return render(request, 'authentication/reset_password.html')


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.warning(request, 'Password link is invalid. Please request a new one.')
                return render(request, 'authentication/reset_password.html')

            messages.success(request, 'Password reset successfully')
            return redirect('auth:login')
        except Exception as e:
            pass

        return render(request, 'authentication/set_new_password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }

        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'authentication/set_new_password.html', context)

        if len(password) < 6:
            messages.error(request, 'Password too short. Make sure password length: 6 or more symbols.')
            return render(request, 'authentication/set_new_password.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(request, 'Password reset successfully')
            return redirect('auth:login')
        except Exception as e:
            messages.info(request, 'Something went wrong, try again')
            return render(request, 'authentication/set_new_password.html', context)





