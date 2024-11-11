from django.urls import path, reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'auth'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('validate-username/', csrf_exempt(views.UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email/', csrf_exempt(views.EmailValidationView.as_view()), name='validate-email'),
    path('activate/<uidb64>/<token>', views.VerificationView.as_view(), name='activate'),
]