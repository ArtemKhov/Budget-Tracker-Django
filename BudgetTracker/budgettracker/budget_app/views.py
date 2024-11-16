from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse

from userpreferences.models import UserPreference
from budget_app.models import Category, Expense
from utils import data_mixin
import json

@login_required(login_url='auth:login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = 'Currency not selected'

    context = data_mixin.extra_context
    context['title'] = 'Budget Tracker'
    context['categories'] = categories
    context['expenses'] = expenses
    context['page_obj'] = page_obj
    context['currency'] = currency
    return render(request, 'budget_app/index.html', context=context)

@login_required(login_url='auth:login')
def add_expense(request):
    categories = Category.objects.all()

    context = data_mixin.extra_context
    context['title'] = 'Add Expenses'
    context['categories'] = categories
    context['values'] = request.POST

    if request.method == 'GET':
        return render(request, 'budget_app/add_expense.html', context=context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['expense_date']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'budget_app/add_expense.html', context=context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'budget_app/add_expense.html', context=context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'budget_app/add_expense.html', context=context)

        Expense.objects.create(owner=request.user,
                               amount=amount,
                               description=description,
                               category=category,
                               date=date)
        messages.success(request, 'Expense saved successfully')
        return redirect('home')

def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()

    context = data_mixin.extra_context
    context['title'] = 'Edit Expense'
    context['categories'] = categories
    context['expense'] = expense
    context['values'] = expense

    if request.method == 'GET':
        return render(request, 'budget_app/edit_expense.html', context=context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['expense_date']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'budget_app/edit_expense.html', context=context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'budget_app/edit_expense.html', context=context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'budget_app/add_expense.html', context=context)

        expense.owner = request.user
        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.date = date
        expense.save()

        messages.success(request, 'Expense updated successfully')
        return redirect('home')

def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()

    messages.warning(request, 'Expense was deleted')
    return redirect('home')


def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = (Expense.objects.filter(amount__istartswith=search_str, owner=request.user)
                    | Expense.objects.filter(date__istartswith=search_str, owner=request.user)
                    | Expense.objects.filter(description__icontains=search_str, owner=request.user)
                    | Expense.objects.filter(category__icontains=search_str, owner=request.user))
        data = expenses.values()
        return JsonResponse(list(data), safe=False)



