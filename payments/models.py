from django.db import models
from orders.models import Order

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('Credit Card', 'Credit Card'),
        ('PayPal', 'PayPal'),
        ('Stripe', 'Stripe'),
    )
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=10, default='Pending')
    payment_date = models.DateTimeField(auto_now_add=True)
