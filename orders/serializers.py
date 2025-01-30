from rest_framework import serializers
from .models import Order_Model, OrderItem_Model
from payments.serializers import Payment_Serializer


class OrderItem_Serializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only= True)
    product_price = serializers.DecimalField(source="product.price", max_digits= 10, decimal_places= 2, read_only= True)

    class Meta:
        model = OrderItem_Model
        fields = ['id', 'order', 'product', 'product_name', 'product_price', 'quantity']



class Order_Serializer(serializers.ModelSerializer):
    items = OrderItem_Serializer(many= True, read_only= True)
    payments = Payment_Serializer(many= True)

    class Meta:
        model = Order_Model
        fields = ['id', 'user', 'full_name', 'email', 'phone', 'address', 'total_price', 'shipping_cost', 'order_status', 'order_time', 'items', 'payments']
        
        
        