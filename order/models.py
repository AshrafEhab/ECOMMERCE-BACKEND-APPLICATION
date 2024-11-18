from django.contrib.auth.models import User
from product.models import Product
from django.db import models
from operator import mod
# Create your models here.

class OrderStatus(models.TextChoices):
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"

class PaymentStatus(models.TextChoices):
    PAID = "Paid"
    UNPAID = "Unpaid"

class PaymentMethod(models.TextChoices):
    COD = "COD"
    CARD = "Card"

class Order(models.Model):
    city = models.CharField(max_length=100, default="", blank=False)
    zip_code = models.CharField(max_length=100, default="", blank=False)
    street = models.CharField(max_length=400, default="", blank=False)
    state = models.CharField(max_length=100, default="", blank=False)
    country = models.CharField(max_length=100, default="", blank=False)
    phone_no = models.CharField(max_length=20, default="", blank=False)
    total_price = models.DecimalField(max_digits=7, decimal_places=2, blank=False,default=0)
    payment_status=models.CharField(max_length=50, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_method=models.CharField(max_length=10, choices=PaymentMethod.choices, default=PaymentMethod.COD)
    status=models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PROCESSING)    
    user = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    create_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
         return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL,related_name="orderitems")
    name = models.CharField(max_length=100, default="", blank=False)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)
    def __str__(self) -> str:
        return self.name
