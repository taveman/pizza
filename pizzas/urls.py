from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pizzas import views


router = DefaultRouter()
router.register('pizzas', views.PizzaViewSet)
router.register('pizzas/sizes', views.PizzaSizeViewSet)

app_name = 'pizzas'

urlpatterns = [
    path('', include(router.urls))
]
