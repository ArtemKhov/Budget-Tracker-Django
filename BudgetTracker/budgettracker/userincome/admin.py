from django.contrib import admin

from .models import Source, UserIncome

admin.site.register(UserIncome)
admin.site.register(Source)
