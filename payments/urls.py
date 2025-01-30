from django.urls import path
from .views import *


urlpatterns = [ 
    path('create/', Payment_View.as_view(), name='payment_process'),
    path('success/', PaymentSuccess_View.as_view(), name='payment_success'),
    path('fail/', PaymentFail_View.as_view(), name='payment_fail'),
    path('cancel/', PaymentCancel_View.as_view(), name='payment_cancel'),
]

