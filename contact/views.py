from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Contact_Model
from .serializers import Contact_Serializer
# Create your views here.

class Contact_ViewSet(ModelViewSet):
    queryset = Contact_Model.objects.all()
    serializer_class = Contact_Serializer
    
