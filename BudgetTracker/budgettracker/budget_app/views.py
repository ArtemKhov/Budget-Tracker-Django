from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from utils import data_mixin

@login_required(login_url='auth:login')
def index(request):
    context = data_mixin.extra_context
    context['title'] = 'Budget Tracker'
    return render(request, 'budget_app/index.html', context=context)

@login_required(login_url='auth:login')
def add_expense(request):
    context = data_mixin.extra_context
    context['title'] = 'Add Expenses'
    return render(request, 'budget_app/add_expense.html', context=context)
