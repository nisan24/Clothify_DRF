from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import pytz
# Create your models here.


SIZE_CHOICES = [
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
    ('XXL', 'Extra Extra Large'),
]

RATING_CHOICES = [
    ("⭐", 1),
    ("⭐⭐", 2),
    ("⭐⭐⭐", 3),
    ("⭐⭐⭐⭐", 4),
    ("⭐⭐⭐⭐⭐", 5),
]


GENDER_CHOICES = [
    ('Men', 'Men'),
    ('Women', 'Women'),
    ('Kids', 'Kids'),
]


class Brand_Model(models.Model):
    name = models.CharField(max_length= 200, unique= True)

    def __str__(self):
        return self.name



class Category_Model(models.Model):
    name = models.CharField(max_length= 200)
    slug = models.SlugField(max_length= 255)
    
    def __str__(self):
        return self.name


class Product_Model(models.Model):
    name = models.CharField(max_length= 210)
    image = models.ImageField(upload_to='products/image/')
    price = models.DecimalField(max_digits= 10, decimal_places= 2)
    description = models.TextField()
    color = models.CharField(max_length= 30)
    size = models.CharField(max_length= 20, choices= SIZE_CHOICES)
    gender = models.CharField(max_length= 20, choices= GENDER_CHOICES, null= True)
    create_time = models.DateTimeField(auto_now_add= True)
    category = models.ForeignKey(Category_Model, on_delete= models.CASCADE)
    brand = models.ForeignKey(Brand_Model, on_delete= models.CASCADE)
    
    def get_bangladesh_time(self):
        bangladesh_timezone = pytz.timezone('Asia/Dhaka')
        return self.create_time.astimezone(bangladesh_timezone)

    def __str__(self):
        return self.name


class Review_Model(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Product_Model, on_delete= models.CASCADE, related_name= "reviews")
    rating = models.CharField(max_length= 8,  choices= RATING_CHOICES)
    comment = models.TextField()
    create_time = models.DateTimeField(auto_now_add= True)
    
    class Meta:
        unique_together = ('user', 'product')
        
        
    def get_bangladesh_time(self):
        bangladesh_timezone = pytz.timezone('Asia/Dhaka')
        return self.create_time.astimezone(bangladesh_timezone)
        
        