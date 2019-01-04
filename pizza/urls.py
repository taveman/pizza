from django.urls import path, include

urlpatterns = [
    path('api/', include('pizzas.urls')),
    path('api/', include('orders.urls')),
    path('api/', include('customers.urls')),
]
