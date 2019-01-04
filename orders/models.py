from django.db import models
from core.models import TimeStampedModel
from customers.models import Customers
from pizzas.models import Pizzas, PizzaSizes


class Order(TimeStampedModel):
    """
    An order class
    """
    CANCELED = 'C'
    ACCEPTED = 'A'
    PROCESSING = 'P'
    SENT = 'S'
    DELIVERED = 'D'

    STATES_CHOICES = (
        (CANCELED, 'Canceled'),
        (ACCEPTED, 'Accepted'),
        (PROCESSING, 'Processing'),
        (SENT, 'Sent'),
        (DELIVERED, 'Delivered'),
    )
    customer = models.ForeignKey(Customers, related_name='customer', on_delete=models.SET_NULL, null=True)
    order_state = models.CharField('Order status', max_length=1, null=False, default='A')

    class Meta:
        ordering = ['-created']


class OrderItem(TimeStampedModel):
    """
    An item from an order
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, null=False)
    pizza_name = models.ForeignKey(Pizzas, on_delete=models.SET_NULL, null=True)
    pizza_size = models.ForeignKey(PizzaSizes, on_delete=models.SET_NULL, null=True)
    number_of_pizzas = models.SmallIntegerField('Number of pizzas', null=False)
    is_active = models.BooleanField('Is active', default=True)

    class Meta:
        ordering = ['-created']
