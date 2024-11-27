import json
import os

from django.conf import settings

sidebar_main = [{'title': "Expenses", 'url_name': 'home'},
        {'title': "Income", 'url_name': 'income'},
]

sidebar_summary = [{'title': "Expenses Summary", 'url_name': 'expenses-stats'},
        {'title': "Income Summary", 'url_name': 'income-stats'},
]

sidebar_settings = [{'title': "Change currency type", 'url_name': 'userpreferences'},
]

def load_currency_data():
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r', encoding='UTF-8') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})
    return currency_data

class DataMixin:
    page_title = None
    extra_context = {}

    def __init__(self):
        if self.page_title:
            self.extra_context['title'] = self.page_title

        if 'sidebar_main' not in self.extra_context:
            self.extra_context['sidebar_main'] = sidebar_main

        if 'sidebar_summary' not in self.extra_context:
            self.extra_context['sidebar_summary'] = sidebar_summary

        if 'sidebar_settings' not in self.extra_context:
            self.extra_context['sidebar_settings'] = sidebar_settings

        if 'currency_data' not in self.extra_context:
            self.extra_context['currency_data'] = load_currency_data()

    def get_mixin_context(self, context, **kwargs):
        context['sidebar_main'] = sidebar_main
        context['sidebar_summary'] = sidebar_summary
        context['sidebar_settings'] = sidebar_settings
        context['currency_data'] = load_currency_data()
        context.update(kwargs)
        return context

data_mixin = DataMixin()