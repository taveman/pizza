from rest_framework.serializers import ModelSerializer
from .models import Customers


class CustomerSerializer(ModelSerializer):
    """
    A serializer for Customer model
    """
    class Meta:
        model = Customers
        fields = '__all__'
