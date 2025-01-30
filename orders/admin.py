from django.contrib import admin
from . models import Order_Model, OrderItem_Model
# Register your models here.

admin.site.register(Order_Model)
admin.site.register(OrderItem_Model)


