from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from django.db import transaction
from rest_framework.response import Response
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer, \
                                OrderCreateSerializer, OrderItemCreateSerializer, \
                                ItemSerializer, OrderStatusSerializer, OrderUpdateSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for Orders Model
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('customer', 'order_state')

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action in ('update', 'partial_update'):
            return OrderUpdateSerializer
        return self.serializer_class


class OrderItemsViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for Orders Model
    """
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def create(self, request, *args, **kwargs):
        order_id = kwargs.get('order')
        data = request.data
        data['order'] = order_id
        serializer = OrderItemCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            result = Order.objects.select_for_update().get(id=order_id)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        order_id = kwargs.get('order')
        if not order_id:
            return
        self.queryset = OrderItem.objects.filter(order_id=order_id)
        return super().list(request, *args, **kwargs)


class ItemsViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):
    """
    A viewset for items
    """
    serializer_class = ItemSerializer
    queryset = OrderItem.objects.all()


class OrderItemsStatusViewSet(viewsets.GenericViewSet,
                              mixins.RetrieveModelMixin):
    """
    A viewset for order status
    """
    serializer_class = OrderStatusSerializer
    queryset = Order.objects.all()
