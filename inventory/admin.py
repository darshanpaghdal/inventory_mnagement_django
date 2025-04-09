from django.contrib import admin
from .models import Category, Supplier, Product, StockLog

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone')
    search_fields = ('name', 'contact_person', 'email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'quantity', 'price', 'category', 'is_low_stock')
    list_filter = ('category', 'supplier')
    search_fields = ('name', 'sku', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(StockLog)
class StockLogAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_change', 'change_type', 'created_by', 'created_at')
    list_filter = ('change_type', 'created_at')
    search_fields = ('product__name', 'reason')
    readonly_fields = ('created_at',)
