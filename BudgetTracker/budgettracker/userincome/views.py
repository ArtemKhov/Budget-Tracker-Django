import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect

from userincome.models import Source, UserIncome
from userpreferences.models import UserPreference
from utils import data_mixin


@login_required(login_url='auth:login')
def index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = 'Currency not selected'

    context = data_mixin.extra_context
    context['title'] = 'Income'
    context['sources'] = sources
    context['income'] = income
    context['page_obj'] = page_obj
    context['currency'] = currency
    return render(request, 'userincome/index.html', context=context)

@login_required(login_url='auth:login')
def add_income(request):
    sources = Source.objects.all()

    context = data_mixin.extra_context
    context['title'] = 'Add Income'
    context['sources'] = sources
    context['values'] = request.POST

    if request.method == 'GET':
        return render(request, 'userincome/add_income.html', context=context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['income_date']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'userincome/add_income.html', context=context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'userincome/add_income.html', context=context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'userincome/add_income.html', context=context)

        UserIncome.objects.create(owner=request.user,
                               amount=amount,
                               description=description,
                               source=source,
                               date=date)
        messages.success(request, 'Income saved successfully')
        return redirect('income')


@login_required(login_url='auth:login')
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()

    context = data_mixin.extra_context
    context['title'] = 'Edit Expense'
    context['sources'] = sources
    context['income'] = income
    context['values'] = income

    if request.method == 'GET':
        return render(request, 'userincome/edit_income.html', context=context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['income_date']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'userincome/edit_income.html', context=context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'userincome/edit_income.html', context=context)

        income.amount = amount
        income.description = description
        income.source = source
        income.date = date
        income.save()

        messages.success(request, 'Income updated successfully')
        return redirect('income')


def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()

    messages.warning(request, 'Income was deleted')
    return redirect('income')


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = (UserIncome.objects.filter(amount__istartswith=search_str, owner=request.user)
                    | UserIncome.objects.filter(date__istartswith=search_str, owner=request.user)
                    | UserIncome.objects.filter(description__icontains=search_str, owner=request.user)
                    | UserIncome.objects.filter(source__icontains=search_str, owner=request.user))
        data = income.values()
        return JsonResponse(list(data), safe=False)
