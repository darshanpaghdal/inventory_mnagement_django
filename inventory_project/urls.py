from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from inventory.admin_site import inventory_admin_site

# Register models with our custom admin site
from inventory.models import Category, Supplier, Product, StockLog
inventory_admin_site.register(Category)
inventory_admin_site.register(Supplier)
inventory_admin_site.register(Product)
inventory_admin_site.register(StockLog)

urlpatterns = [
    path('admin/', inventory_admin_site.urls),
    path('api/', include('inventory.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
