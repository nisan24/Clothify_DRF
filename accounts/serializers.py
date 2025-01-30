from rest_framework import serializers
from django.contrib.auth.models import User
from . models import *


class UserRegistration_Serializers(serializers.ModelSerializer): 
    first_name = serializers.CharField(required = True)
    last_name = serializers.CharField(required = True)
    confirm_password = serializers.CharField(write_only = True, required = True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        
        
    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
          
          
        if password != confirm_password:
            raise serializers.ValidationError({'error': "Passwords do not match"})
        
        
        if User.objects.filter(username= username).exists():
            raise serializers.ValidationError({'error': 'username already exists'})
        
        
        if User.objects.filter(email= email).exists():
            raise serializers.ValidationError({'error': 'Email already exists'})
        
        
        account = User(username = username, first_name = first_name, last_name = last_name, email = email)
        account.set_password(password)
        account.is_active = False
        account.save()
        return account
    
    
    
class UserLogin_Serializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    
    
    
    
class UserProfile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        
        
        