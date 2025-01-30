from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Order_View, MyOrders_View

router = DefaultRouter()
# router.register('orders', Order_ViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path("orders/", Order_View.as_view(), name= 'order'),
    path("order/list/", MyOrders_View.as_view(), name= 'my-orders'),
    path("order/list/<int:order_id>/", MyOrders_View.as_view(), name="order-detail"),

]
