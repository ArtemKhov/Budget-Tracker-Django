from django.contrib import admin
from .models import Expense, Category

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['amount', 'description', 'category', 'date', 'owner']
    list_display_links = ['amount', 'description', 'category', 'owner']
    list_per_page = 5
    ordering = ['-date', 'amount', 'category', 'owner']
    search_fields = ['amount', 'description', 'category', 'date', 'owner']
    list_filter = ['category']




admin.site.register(Category)
