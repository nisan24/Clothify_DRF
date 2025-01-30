from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from .models import Payment_Model, Order_Model
from wishlist.models import Cart_Model
from sslcommerz_lib import SSLCOMMERZ
import uuid
from django.http import HttpResponseRedirect
from rest_framework.authentication import TokenAuthentication
# Create your views here.

class Payment_View(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        order_id = request.data.get('order_id')

        try:
            order = Order_Model.objects.get(id= order_id)
        except Order_Model.DoesNotExist:
            return Response(
                {"message": "Order not found."}, 
                status= status.HTTP_404_NOT_FOUND
            )

        if order.payments.filter(payment_status="Completed").exists():
            return Response(
                {"message": "This order has already been paid for."}, 
                status= status.HTTP_400_BAD_REQUEST
            )

        
        settings_data = {
            "store_id": settings.STORE_ID,
            "store_pass": settings.STORE_PASS,
            "issandbox": settings.IS_SANDBOX,
        }

        sslcz = SSLCOMMERZ(settings_data)

        # transaction ID
        transaction_id = f"TXN-O{order_id}U{request.user.id}-{str(uuid.uuid4())[:8].upper()}"

        post_body = {
            "total_amount": float(order.total_price),
            "currency": "BDT",
            "tran_id": transaction_id,
            "success_url": f"https://clothify-yzcm.onrender.com/api/payment/success/",
            "fail_url": "https://clothify-yzcm.onrender.com/api/payment/fail/",
            "cancel_url": "https://clothify-yzcm.onrender.com/api/payment/cancel/",
            "emi_option": 0,
            "cus_name": order.full_name,
            "cus_email": order.email,
            "cus_phone": order.phone,
            "cus_add1": order.address,
            "cus_city": "Dhaka",
            "cus_country": "Bangladesh",
            "shipping_method": "NO",
            "product_name": f"Order {order.id}",
            "num_of_item": order.items.count(),
            "product_category": "Order",
            "product_profile": "general",
        }

        response = sslcz.createSession(post_body)

        if response.get("status") == "SUCCESS":
            try:
                Payment_Model.objects.create(
                    user= request.user,
                    order= order,
                    amount= order.total_price,
                    payment_status= "Pending",
                    transaction_id= transaction_id,
                )

                return Response(
                    {
                        "status": "success",
                        "tran_id": transaction_id,
                        "message": f"Payment successfully! orderID: {order.id}",
                        "payment_url": response.get("GatewayPageURL"),
                    },
                    status= status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {
                        "status": "error",
                        "message": "Failed to create payment entry.",
                        "details": str(e),
                    },
                    status= status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:    
            order.order_status = "Failed"
            order.save()
            
            return Response(
                {
                    "status": "error",
                    "message": "Payment session creation failed.",
                    "details": response,
                },
                status= status.HTTP_400_BAD_REQUEST,
            )

# ===


class PaymentSuccess_View(APIView):
    def post(self, request):
        tran_id = request.data.get('tran_id')
        
        if not tran_id:
            return Response({"message": "Transaction ID is required"}, status= status.HTTP_400_BAD_REQUEST)
        
        try:
            payment = Payment_Model.objects.get(transaction_id= tran_id)
            payment.payment_status = 'Completed'
            payment.save()

            order = payment.order
            order.order_status = 'Completed'
            order.save()
            
            Cart_Model.objects.filter(user= order.user).delete()

            return HttpResponseRedirect("http://127.0.0.1:5501/my_order.html")
            # return Response({
            #     "message": "Payment successful!",
            #     "order_id": order.id,
            #     "transaction_id": tran_id,
            #     "status": "success"
            # }, status= status.HTTP_200_OK)

        except Payment_Model.DoesNotExist:
            return Response({"message": "Payment not found"}, status= status.HTTP_404_NOT_FOUND)


class PaymentFail_View(APIView):
    def post(self, request):
        tran_id = request.data.get('tran_id')
        
        try:
            payment = Payment_Model.objects.get(transaction_id= tran_id)
            payment.payment_status = 'Failed'
            payment.save()


            order = payment.order
            order.order_status = 'Failed'
            order.save()

            return HttpResponseRedirect("http://127.0.0.1:5501/cart.html")
            # return Response({'message': 'Payment failed!'}, status= status.HTTP_200_OK)
        except Payment_Model.DoesNotExist:
            return Response({'message': 'Payment not found'}, status= status.HTTP_404_NOT_FOUND)



class PaymentCancel_View(APIView):
    def post(self, request):
        tran_id = request.data.get('tran_id')
        
        try:
            payment = Payment_Model.objects.get(transaction_id= tran_id)
            payment.payment_status = 'Failed'
            payment.save()

            order = payment.order
            order.order_status = 'Failed'
            order.save()
            
            
            return HttpResponseRedirect("http://127.0.0.1:5501/cart.html")
            # return Response({'message': 'Payment cancelled!'}, status= status.HTTP_200_OK)
        except Payment_Model.DoesNotExist:
            return Response({'message': 'Payment not found'}, status= status.HTTP_404_NOT_FOUND)
        
        
        
        