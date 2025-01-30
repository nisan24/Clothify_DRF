from django.db import models
from django.contrib.auth.models import User
from products.models import Product_Model

# Create your models here.

class Wishlist_Model(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Product_Model, on_delete= models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Cart_Model(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product_Model, on_delete= models.CASCADE)
    quantity = models.PositiveIntegerField(default= 1)

    def __str__(self):
        return f"{self.user.username} --- {self.product.name} * {self.quantity}"

