from django.db import models
from django.contrib.auth.models import User
from products.models import Product_Model

# Create your models here.

STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Completed", "Completed"),
]

class Order_Model(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='orders')
    full_name = models.CharField(max_length= 255)
    email = models.EmailField()
    phone = models.CharField(max_length= 20)
    address = models.TextField()
    total_price = models.DecimalField(max_digits= 10, decimal_places= 2)
    shipping_cost = models.DecimalField(max_digits= 10, decimal_places= 2, default= 150.00)
    order_status = models.CharField(max_length= 15, choices= STATUS_CHOICES, default= 'Pending')
    order_time = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"



class OrderItem_Model(models.Model):
    order = models.ForeignKey(Order_Model, on_delete= models.CASCADE, related_name='items')
    product = models.ForeignKey(Product_Model, on_delete= models.CASCADE, null= True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        if self.product:
            return f"{self.quantity} * {self.product.name} ---> (Order {self.order.id})"
        return f"{self.quantity} -- (Order {self.order.id})"

        