from .models import Pizzas, PizzaSizes
from rest_framework.serializers import ModelSerializer


class PizzaSerializer(ModelSerializer):
    """
    A Pizzas model general serializer
    """
    class Meta:
        model = Pizzas
        fields = ('id', 'name', 'created', 'updated')
        read_only_fields = ('id', )


class PizzaSizeSerializer(ModelSerializer):
    """
    A PizzaSizes model general serializer
    """
    class Meta:
        model = PizzaSizes
        fields = ('id', 'sizename', 'created', 'updated')
        read_only_fileds = ('id', )
