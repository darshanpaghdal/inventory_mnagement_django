from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F
from .models import Product, StockLog
from .serializers import ProductSerializer, StockLogSerializer, StockAlertSerializer

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can create products'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can update products'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can delete products'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        supplier = self.request.query_params.get('supplier', None)
        low_stock = self.request.query_params.get('low_stock', None)

        if category:
            queryset = queryset.filter(category__name=category)
        if supplier:
            queryset = queryset.filter(supplier__name=supplier)
        if low_stock == 'true':
            queryset = queryset.filter(quantity__lte=F('low_stock_threshold'))

        return queryset

    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can adjust stock'},
                status=status.HTTP_403_FORBIDDEN
            )

        product = self.get_object()
        quantity_change = request.data.get('quantity_change')
        change_type = request.data.get('change_type')
        reason = request.data.get('reason')

        if not all([quantity_change, change_type, reason]):
            return Response(
                {'error': 'Missing required fields: quantity_change, change_type, reason'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity_change = int(quantity_change)
            if change_type == 'remove' and product.quantity < quantity_change:
                return Response(
                    {'error': 'Insufficient stock'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update product quantity
            if change_type == 'add':
                product.quantity += quantity_change
            elif change_type == 'remove':
                product.quantity -= quantity_change
            else:
                return Response(
                    {'error': 'change_type field has only two values supported. 1) add 2) remove'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            product.save()

            # Create stock log
            StockLog.objects.create(
                product=product,
                quantity_change=quantity_change,
                change_type=change_type,
                reason=reason,
                created_by=request.user
            )

            return Response(ProductSerializer(product).data)
        except ValueError:
            return Response(
                {'error': 'Invalid quantity_change value'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False)
    def inventory_value(self, request):
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can view inventory value'},
                status=status.HTTP_403_FORBIDDEN
            )
        total_value = Product.objects.aggregate(
            total=Sum(F('quantity') * F('price'))
        )['total'] or 0
        return Response({'total_inventory_value': total_value})

    @action(detail=False)
    def stock_alerts(self, request):
        """Get all products with low stock"""
        low_stock_products = Product.objects.filter(quantity__lte=F('low_stock_threshold'))
        serializer = StockAlertSerializer(low_stock_products, many=True)
        return Response({
            'count': low_stock_products.count(),
            'alerts': serializer.data
        })

    @action(detail=False)
    def report(self, request):
        """Generate inventory report"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can view reports'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get filter parameters
        category = request.query_params.get('category')
        supplier = request.query_params.get('supplier')
        stock_level = request.query_params.get('stock_level')  # 'low', 'normal', or None
        sort_by = request.query_params.get('sort_by', 'quantity')  # 'quantity' or 'value'
        sort_order = request.query_params.get('sort_order', 'asc')  # 'asc' or 'desc'

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

        # Calculate total inventory value
        total_value = queryset.aggregate(
            total=Sum(F('quantity') * F('price'))
        )['total'] or 0

        # Apply sorting
        if sort_by == 'quantity':
            order_field = 'quantity'
        else:  # value
            order_field = F('quantity') * F('price')
        
        if sort_order == 'desc':
            order_field = order_field.desc()
        
        queryset = queryset.order_by(order_field)

        # Serialize the results
        serializer = ProductSerializer(queryset, many=True)

        return Response({
            'total_inventory_value': total_value,
            'product_count': queryset.count(),
            'low_stock_count': queryset.filter(quantity__lte=F('low_stock_threshold')).count(),
            'products': serializer.data
        })

class StockLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockLog.objects.all()
    serializer_class = StockLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = StockLog.objects.all()
        product_id = self.request.query_params.get('product', None)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset
