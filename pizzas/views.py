from rest_framework import viewsets, mixins
from pizzas.serializers import PizzaSerializer, PizzaSizeSerializer
from pizzas.models import Pizzas, PizzaSizes


class PizzaViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for Pizza Model
    """
    serializer_class = PizzaSerializer
    queryset = Pizzas.objects.all()

    def get_queryset(self):
        return self.queryset.filter(is_deleted=False)


class PizzaSizeViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin):
    """
    A ViewSet for PizzaSize Model
    """
    serializer_class = PizzaSizeSerializer
    queryset = PizzaSizes.objects.all()

