from django.db import models
from orders.models import Order
class Shipping(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping')
    provider = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    estimated_delivery = models.DateTimeField()
    
class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_address')
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)