# inventory/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, Product, Sale, Purchase, Expense, SalesSummary, PurchaseSummary, ExpenseSummary, ExpenseByCategory, CustomUser

User = get_user_model()


class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ['email', 'name', 'is_active', 'is_staff']
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}
         ),
    )
    search_fields = ['email', 'name']
    ordering = ['email']


# Custom admin for Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'stock_quantity', 'rating']  # Include ID and stock quantity
    search_fields = ['name']  # Optional: Add search functionality

# Register your custom user admin
admin.site.register(CustomUser, CustomUserAdmin)

# Register other models
admin.site.register(Profile)
admin.site.register(Product, ProductAdmin)  # Register Product with custom admin
admin.site.register(Sale)
admin.site.register(Purchase)
admin.site.register(Expense)
admin.site.register(SalesSummary)
admin.site.register(PurchaseSummary)
admin.site.register(ExpenseSummary)
admin.site.register(ExpenseByCategory)
