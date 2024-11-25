from django.db import models
from django.contrib.auth.models import User

class Category (models.TextChoices):
    ELECTRONICS = 'Electronics'
    FURNITURE = 'Furniture'
    CLOTHES = 'Clothes'
    FOOD = 'Food'

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200, default="", blank=False)
    description = models.TextField(max_length=1000, default="", blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    brand = models.CharField(max_length=200, default="", blank=False)
    category = models.CharField(max_length=40, choices=Category.choices)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    createAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    def __str__(self) -> str:
        return self.name
    
class Review(models.Model):
    product = models.ForeignKey(Product,null=True, on_delete=models.CASCADE,related_name='reviews')
    user = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField(default=0)
    comment = models.TextField(max_length=1000, default="", blank=False)
    createAt = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.comment

    

