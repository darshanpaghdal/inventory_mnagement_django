from django.contrib.admin import AdminSite
from django.db.models import F
from inventory.models import Product

class InventoryAdminSite(AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        # Add low stock products to the context
        low_stock_products = Product.objects.filter(quantity__lte=F('low_stock_threshold'))
        context['low_stock_products'] = low_stock_products
        return context

# Create an instance of our custom admin site
inventory_admin_site = InventoryAdminSite(name='inventory_admin') 