from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders import views


router = DefaultRouter()
router.register('orders', views.OrderViewSet, basename='orders')
router.register('orders/(?P<order>[0-9]+)/items', views.OrderItemsViewSet, basename='orderitems')
router.register('orders/status', views.OrderItemsStatusViewSet, basename='orderstatus')
router.register('items', views.ItemsViewSet, basename='items')

app_name = 'orders'

# for url in router.urls:
#     print(url.__dict__)

urlpatterns = [
    path('', include(router.urls))
]
