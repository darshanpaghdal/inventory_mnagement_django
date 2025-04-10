from django.contrib import admin
from django.db.models import F
from django.utils.html import format_html
from .models import Category, Supplier, Product, StockLog

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone')
    search_fields = ('name', 'contact_person', 'email')

class LowStockFilter(admin.SimpleListFilter):
    title = 'stock status'
    parameter_name = 'stock_status'

    def lookups(self, request, model_admin):
        return (
            ('low', 'Low Stock'),
            ('normal', 'Normal Stock'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(quantity__lte=F('low_stock_threshold'))
        if self.value() == 'normal':
            return queryset.filter(quantity__gt=F('low_stock_threshold'))

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'quantity', 'price', 'category', 'get_stock_status', 'low_stock_threshold')
    list_filter = ('category', 'supplier', LowStockFilter)
    search_fields = ('name', 'sku', 'description')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['send_low_stock_alert']

    def get_stock_status(self, obj):
        if obj.is_low_stock:
            return format_html(
                '<span style="color: red; font-weight: bold;">LOW STOCK ({})</span>',
                obj.quantity
            )
        return format_html(
            '<span style="color: green;">Normal ({})</span>',
            obj.quantity
        )
    get_stock_status.short_description = 'Stock Status'

    def changelist_view(self, request, extra_context=None):
        # Get low stock products
        low_stock_products = Product.objects.filter(quantity__lte=F('low_stock_threshold'))
        
        if low_stock_products.exists():
            # Add warning message
            self.message_user(
                request,
                f'Warning: {low_stock_products.count()} products are low on stock!',
                level='WARNING'
            )
            
            # Add low stock products to context
            if extra_context is None:
                extra_context = {}
            extra_context['low_stock_products'] = low_stock_products

        return super().changelist_view(request, extra_context=extra_context)

    def send_low_stock_alert(self, request, queryset):
        low_stock_products = queryset.filter(quantity__lte=F('low_stock_threshold'))
        count = low_stock_products.count()
        self.message_user(
            request,
            f'Alert: {count} products are low on stock!',
            level='WARNING'
        )
    send_low_stock_alert.short_description = 'Send low stock alert'

@admin.register(StockLog)
class StockLogAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_change', 'change_type', 'created_by', 'created_at')
    list_filter = ('change_type', 'created_at')
    search_fields = ('product__name', 'reason')
    readonly_fields = ('created_at',)
