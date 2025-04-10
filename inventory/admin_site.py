from django.contrib.admin import AdminSite
from django.db.models import Sum, F, Count, Q
from django.shortcuts import render
from django.urls import path
from inventory.models import Product, Category, Supplier

class InventoryAdminSite(AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('reports/', self.admin_view(self.reports_view), name='inventory-reports'),
        ]
        return custom_urls + urls

    def reports_view(self, request):
        # Get filter parameters
        category = request.GET.get('category')
        supplier = request.GET.get('supplier')
        stock_level = request.GET.get('stock_level')
        sort_param = request.GET.get('sort', 'quantity_desc')
        
        # Base queryset
        queryset = Product.objects.all()

        # Apply filters
        if category:
            queryset = queryset.filter(category__name=category)
        if supplier:
            queryset = queryset.filter(supplier__name=supplier)
        if stock_level == 'low':
            queryset = queryset.filter(quantity__lte=F('low_stock_threshold'))
        elif stock_level == 'normal':
            queryset = queryset.filter(quantity__gt=F('low_stock_threshold'))

        # Calculate total inventory value for filtered products
        total_inventory_value = queryset.aggregate(
            total=Sum(F('quantity') * F('price'))
        )['total'] or 0

        # Apply sorting
        if sort_param == 'quantity_asc':
            queryset = queryset.order_by('quantity')
        elif sort_param == 'quantity_desc':
            queryset = queryset.order_by('-quantity')
        elif sort_param == 'value_asc':
            queryset = queryset.annotate(
                total_value=F('quantity') * F('price')
            ).order_by('total_value')
        else:  # value_desc
            queryset = queryset.annotate(
                total_value=F('quantity') * F('price')
            ).order_by('-total_value')

        # Get all categories and suppliers for filter dropdowns
        categories = Category.objects.all()
        suppliers = Supplier.objects.all()

        context = {
            'total_inventory_value': total_inventory_value,
            'all_products': queryset.select_related('category', 'supplier'),
            'categories': categories,
            'suppliers': suppliers,
            'category': category,
            'supplier': supplier,
            'stock_level': stock_level,
            'title': 'Inventory Reports',
            'site_header': self.site_header,
            'site_title': self.site_title,
            'index_title': self.index_title,
        }
        return render(request, 'admin/inventory/reports.html', context)

    def each_context(self, request):
        context = super().each_context(request)
        # Add low stock products to the context
        low_stock_products = Product.objects.filter(quantity__lte=F('low_stock_threshold'))
        context['low_stock_products'] = low_stock_products
        return context

# Create an instance of our custom admin site
inventory_admin_site = InventoryAdminSite(name='inventory_admin') 