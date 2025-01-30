from rest_framework import serializers
from .models import Contact_Model

class Contact_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Contact_Model
        fields = ['id', 'name', 'email', 'message', 'time']
        
