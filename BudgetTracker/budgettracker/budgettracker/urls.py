from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('budget_app.urls')),
    path('auth/', include('authentication.urls', namespace='auth')),
    path('preferences/', include('userpreferences.urls')),
    path('income/', include('userincome.urls')),
]
