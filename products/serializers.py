from rest_framework import serializers
from .models import *

class Brand_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Brand_Model
        fields = '__all__'
    

class Category_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Category_Model
        fields = '__all__'
        

class Review_Serializer(serializers.ModelSerializer):
    user = serializers.CharField(source= 'user.username', read_only= True)
    product_name = serializers.CharField(source= 'product.name', read_only= True)

    class Meta:
        model = Review_Model
        fields = ['id', 'user', 'product', 'product_name', 'rating', 'comment', 'create_time']        
 
 
        
class Product_Serializer(serializers.ModelSerializer):
    brand = serializers.CharField(source= 'brand.name', read_only= True)
    category = serializers.CharField(source= 'category.name', read_only= True)
    reviews = Review_Serializer(many= True)

    class Meta:
        model = Product_Model
        fields = ['id', 'name', 'price', 'size', 'color', 'image', 'category', 'brand', 'description', 'create_time', 'reviews']


