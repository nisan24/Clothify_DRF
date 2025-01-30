from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from .models import Order_Model, OrderItem_Model
from wishlist.models import Cart_Model
from .serializers import Order_Serializer


class Order_View(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        user = request.user

        cart_items = Cart_Model.objects.filter(user= user)

        if not cart_items.exists():
            return Response({"error": "Your cart is empty!"}, status= status.HTTP_400_BAD_REQUEST)

        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        shipping_cost = 150
        total_amount = subtotal + shipping_cost

        full_name = request.data.get("full_name")
        email = request.data.get("email")
        phone = request.data.get("phone")
        address = request.data.get("address")

        if not (full_name and email and phone and address):
            return Response({"error": "All fields are required."},
                            status= status.HTTP_400_BAD_REQUEST)

        order = Order_Model.objects.create(
            user= user,
            full_name= full_name,
            email= email,
            phone= phone,
            address= address,
            total_price= total_amount,
            shipping_cost= shipping_cost,
            order_status="Pending",
        )

        for cart_item in cart_items:
            OrderItem_Model.objects.create(
                order= order,
                product= cart_item.product,
                quantity= cart_item.quantity,
            )

        # cart_items.delete()

        serializer = Order_Serializer(order)
        return Response({"message": "Order created successfully!", "order": serializer.data}, status= status.HTTP_201_CREATED)




class MyOrders_View(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, order_id= None):
        user = request.user

        if order_id:
            try:
                order = Order_Model.objects.get(user= user, id= order_id)
                serializer = Order_Serializer(order)
                return Response({"order": serializer.data}, status= status.HTTP_200_OK)
            except Order_Model.DoesNotExist:
                return Response({"error": "Order not found!"}, status= status.HTTP_404_NOT_FOUND)

        orders = Order_Model.objects.filter(user= user).order_by('-order_time')

        if not orders.exists():
            return Response({"message": "No orders found!"}, status= status.HTTP_200_OK)

        serializer = Order_Serializer(orders, many= True)
        return Response({"orders": serializer.data}, status= status.HTTP_200_OK)

