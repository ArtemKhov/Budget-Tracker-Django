import csv
import datetime
import json

import xlwt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render

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

def income_source_summary(request):
    today_date = datetime.date.today()
    six_month_ago = today_date - datetime.timedelta(days=30*6)
    sources = UserIncome.objects.filter(owner=request.user, date__gte=six_month_ago, date__lte=today_date)
    final_rep = {}

    def get_source(source):
        return source.source
    source_list = list(set(map(get_source, sources)))

    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = sources.filter(source=source)
        for item in filtered_by_source:
            amount += item.amount
        return amount

    for source in sources:
        for category in source_list:
            final_rep[category] = get_income_source_amount(category)

    return JsonResponse({"income_source_data": final_rep}, safe=False)

def stats_view(request):
    context = data_mixin.extra_context
    context['title'] = 'Income Summary'
    return render(request, 'userincome/stats.html', context)

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        f'attachment; filename=Income {datetime.datetime.now().strftime("%Y-%m-%d")}.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Source', 'Date'])

    incomes = UserIncome.objects.filter(owner=request.user)

    for income in incomes:
        writer.writerow([income.amount, income.description, income.source, income.date])

    return response

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = \
        f'attachment; filename=Income {datetime.datetime.now().strftime("%Y-%m-%d")}.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Income')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'Source', 'Date']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style.font.bold = xlwt.XFStyle()
    rows = UserIncome.objects.filter(owner=request.user).values_list('amount', 'description', 'source', 'date')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response