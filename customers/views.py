from rest_framework import viewsets
from customers.models import Customers
from customers.serializers import CustomerSerializer


class CustomersViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for Pizza Model
    """
    serializer_class = CustomerSerializer
    queryset = Customers.objects.all()

