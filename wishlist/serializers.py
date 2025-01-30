from rest_framework import serializers
from .models import Wishlist_Model, Cart_Model


class Wishlist_Serializer(serializers.ModelSerializer):
    user = serializers.CharField(source= 'user.username', read_only= True)
    product_name = serializers.CharField(source= 'product.name', read_only= False)
    product_id = serializers.CharField(source= 'product.id', read_only= True)
    product_price = serializers.DecimalField(source= 'product.price', max_digits= 10, decimal_places= 2, read_only= True)
    product_image = serializers.ImageField(source= 'product.image', read_only= True)
    class Meta:
        model = Wishlist_Model
        fields = ['id', 'user', 'product_id', 'product_name', 'product_price', 'product_image']


class Cart_Serializer(serializers.ModelSerializer):
    user = serializers.CharField(source= 'user.username', read_only= True)
    product_name = serializers.CharField(source= 'product.name', read_only= True)
    product_id = serializers.CharField(source= 'product.id', read_only= True)
    product_price = serializers.DecimalField(source= 'product.price', max_digits= 10, decimal_places= 2, read_only= True)
    product_image = serializers.ImageField(source= 'product.image', read_only= True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart_Model
        # fields = "__all__"
        fields = ['id', 'user', 'product_id', 'product_name', 'product_price', 'product_image' , 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price 
    
    