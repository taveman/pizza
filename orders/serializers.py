from .models import Order, OrderItem
from pizzas.models import Pizzas, PizzaSizes
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, ValidationError


class OrderSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'customer', 'items', 'created', 'updated', 'order_state')
        read_only_fields = ('id', )


class OrderCreateSerializer(ModelSerializer):

    def validate(self, data):
        if not data.get('customer'):
            raise ValidationError('customer field must be specified')
        return super().validate(data)

    class Meta:
        model = Order
        fields = ('id', 'customer')
        read_only_fields = ('id', )


class OrderUpdateSerializer(ModelSerializer):

    def update(self, instance, validated_data):
        if instance.order_state in (Order.DELIVERED, Order.SENT):
            raise ValidationError('Order can\'t be change already. It is in state: {}'.format(instance.order_state))
        instance.customer = validated_data.get('customer', instance.customer)
        instance.order_state = validated_data.get('order_state', instance.order_state)
        instance.save()
        return instance

    class Meta:
        model = Order
        fields = ('id', 'customer', 'order_state')
        read_only_fields = ('id', )


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'pizza_name', 'pizza_size', 'number_of_pizzas', 'is_active', 'created', 'updated')
        read_only_fields = ('id', )


class OrderItemCreateSerializer(ModelSerializer):
    """
    Order can only be in states Accepted or Processing
    """
    pizza_name = PrimaryKeyRelatedField(queryset=Pizzas.objects.filter(is_deleted=False))
    pizza_size = PrimaryKeyRelatedField(queryset=PizzaSizes.objects.filter(is_deleted=False))
    order = PrimaryKeyRelatedField(queryset=Order.objects.filter(order_state__in=["A", "P"]))

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'pizza_name', 'pizza_size', 'number_of_pizzas')
        read_only_fields = ('id', )


class ItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'pizza_name', 'pizza_size', 'number_of_pizzas')
        read_only_fields = ('id', )


class OrderStatusSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = ('order_state', )
        read_only_fields = ('order_state', )
