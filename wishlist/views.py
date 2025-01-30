from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from  .models import Wishlist_Model, Cart_Model, Product_Model
from . serializers import Wishlist_Serializer, Cart_Serializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class Add_Wishlist_View(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product")

        if not product_id:
            return Response({"error": "Product ID is required"}, status= status.HTTP_400_BAD_REQUEST)

        if Wishlist_Model.objects.filter(user= request.user, product_id= product_id).exists():
            return Response({"detail": "Already in Wishlist!"}, status= status.HTTP_400_BAD_REQUEST)

        wishlist_item = Wishlist_Model.objects.create(user= request.user, product_id= product_id)
        serializer = Wishlist_Serializer(wishlist_item)
        return Response({"message": "Added to Wishlist", "wishlist_item": serializer.data}, status= status.HTTP_201_CREATED)



class Wishlist_ListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist_items = Wishlist_Model.objects.filter(user= request.user)

        if not wishlist_items.exists():
            return Response({"message": "Your wishlist is empty!"}, status= status.HTTP_200_OK)

        serializer = Wishlist_Serializer(wishlist_items, many= True)

        return Response({
            "wishlist_items": serializer.data,
            "total_items": wishlist_items.count()
        }, status= status.HTTP_200_OK)



class Wishlist_Check_View(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        wishlist_exists = Wishlist_Model.objects.filter(user= request.user, product_id= product_id).exists()
        return Response({"wishlist": wishlist_exists}, status= status.HTTP_200_OK)



class Wishlist_Remove_View(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        wishlist_item = Wishlist_Model.objects.filter(user= request.user, product_id= product_id).first()

        if wishlist_item:
            wishlist_item.delete()
            return Response({"message": "Product removed from wishlist"}, status= status.HTTP_200_OK)

        return Response({"error": "Product not found in wishlist"}, status= status.HTTP_404_NOT_FOUND)



class AddToCart(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            return Response({"error": "Product ID is required!"}, status= status.HTTP_400_BAD_REQUEST)

        try:
            product = Product_Model.objects.get(id= product_id)
            
        except Product_Model.DoesNotExist:
            return Response({"error": "Product not found!!"}, status= status.HTTP_404_NOT_FOUND)

        quantity = max(int(quantity), 1)

        cart_item, created = Cart_Model.objects.get_or_create(user= user, product= product)

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()
        
        serializer = Cart_Serializer(cart_item)
        return Response({"message": "Product added to cart", "cart_item": serializer.data}, status= status.HTTP_201_CREATED)


    def put(self, request):
        user = request.user
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        if not product_id or not quantity:
            return Response({"error": "Product ID and Quantity required!"}, status= status.HTTP_400_BAD_REQUEST)

        try:
            product = Product_Model.objects.get(id= product_id)
        except Product_Model.DoesNotExist:
            return Response({"error": "Product not found!"}, status= status.HTTP_404_NOT_FOUND)

        quantity = max(int(quantity), 1)

        try:
            cart_item = Cart_Model.objects.get(user= user, product= product)
            cart_item.quantity = quantity
            cart_item.save()

            total_price = cart_item.quantity * product.price

            cart_items = Cart_Model.objects.filter(user= user)
            subtotal = sum(item.quantity * item.product.price for item in cart_items)
            shipping_cost = 150
            total_amount = subtotal + shipping_cost

            serializer = Cart_Serializer(cart_item)

            return Response({
                "message": "Cart item updated",
                "cart_item": serializer.data,
                "subtotal": subtotal,
                "shipping_cost": shipping_cost,
                "total_amount": total_amount,
            }, status= status.HTTP_200_OK)
        except Cart_Model.DoesNotExist:
            return Response({"error": "Item not found in cart!"}, status= status.HTTP_404_NOT_FOUND)


class Cart_ListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = Cart_Model.objects.filter(user= request.user)

        if not cart_items.exists():
            return Response({
                "message": "Your cart is empty!",
                "cart_items": [],
                "total_items": 0,
                "total_quantity": 0,
                "subtotal": 0.00,
                "shipping_cost": 0.00,
                "total_amount": 0.00,
            }, status= status.HTTP_200_OK)

        serializer = Cart_Serializer(cart_items, many= True)

        total_quantity = sum(item.quantity for item in cart_items)
        subtotal = sum(item.quantity * item.product.price for item in cart_items)
        shipping_cost = 150
        total_amount = subtotal + shipping_cost

        return Response({
            "message": "Cart details!",
            "cart_items": serializer.data,
            "total_items": cart_items.count(),
            "total_quantity": total_quantity,
            "subtotal": subtotal,
            "shipping_cost": shipping_cost,
            "total_amount": total_amount,
        }, status= status.HTTP_200_OK)




class CartItem_Remove_view(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        user = request.user
        try:
            cart_item = Cart_Model.objects.get(user= user, product_id= product_id)
            cart_item.delete()
            return Response({"message": "Product removed from cart"}, status= status.HTTP_200_OK)
        
        except Cart_Model.DoesNotExist:
            return Response({"error": "Product not found in cart"}, status= status.HTTP_404_NOT_FOUND)

