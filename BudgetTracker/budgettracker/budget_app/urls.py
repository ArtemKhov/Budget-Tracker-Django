from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('add-expense/', views.add_expense, name='add-expense'),
    path('edit-expense/<int:id>', views.expense_edit, name='edit-expense'),
    path('delete-expense/<int:id>', views.delete_expense, name='delete-expense'),
    path('search-expenses/', csrf_exempt(views.search_expenses), name='search-expenses'),
    path('expense-category-summary/', views.expense_category_summary, name='expense-category-summary'),
    path('stats/', views.stats_view, name='stats'),
    path('export-csv/', views.export_csv, name='export-csv'),
    path('export-excel/', views.export_excel, name='export-excel'),
]