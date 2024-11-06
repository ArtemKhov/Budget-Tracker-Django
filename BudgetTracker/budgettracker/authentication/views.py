from django.shortcuts import render
from django.views import View

from views import sidebar_main, sidebar_summary


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html',
                      context={'title': 'Registration',
                               'sidebar_main': sidebar_main,
                               'sidebar_summary': sidebar_summary,
                               })

