from rest_framework import serializers
from . models import Payment_Model


class Payment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Payment_Model
        fields = ['id', 'user', 'order', 'amount', 'transaction_id', 'payment_status', 'payment_time']
        
        