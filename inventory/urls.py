from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, StockLogViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'stock-logs', StockLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 