from django.shortcuts import render

sidebar_main = [{'title': "Dashboard", 'url_name': 'home'},
        {'title': "Expenses", 'url_name': 'home'},
        {'title': "Income", 'url_name': 'home'},
]

sidebar_summary = [{'title': "Expenses Summary", 'url_name': 'home'},
        {'title': "Income Summary", 'url_name': 'home'},
]


def index(request):
    context = {
        'title': 'Budget Tracker',
        'sidebar_main': sidebar_main,
        'sidebar_summary': sidebar_summary,
    }
    return render(request, 'budget_app/index.html', context=context)


def add_expense(request):
    context = {
        'title': 'Add Expense',
        'sidebar_main': sidebar_main,
        'sidebar_summary': sidebar_summary,
    }
    return render(request, 'budget_app/add_expense.html', context=context)
