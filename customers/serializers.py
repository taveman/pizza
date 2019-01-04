from rest_framework.serializers import ModelSerializer
from .models import Customers


class CustomerSerializer(ModelSerializer):

    class Meta:
        model = Customers
        fields = '__all__'
