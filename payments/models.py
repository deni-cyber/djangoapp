from django.db import models
from orders.models import Order
from django.contrib.auth import get_user_model

User = get_user_model()
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    order = models.OneToOneField(Order, on_delete=models.CASCADE)  # One payment per order
    merchant_request_id = models.CharField(max_length=255, blank=True, null=True)
    checkout_request_id = models.CharField(max_length=255, blank=True, null=True)
    receipt_number = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.CharField(max_length=20, blank=True, null=True)
    result_desc = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Success', 'Success'), ('Failed', 'Failed')], default='Pending')
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"
    
class PaymentCallbackLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    raw_data = models.JSONField()  # Stores the full callback payload
    processed = models.BooleanField(default=False)  # Has it been processed successfully?

    def __str__(self):
        return f"Callback at {self.timestamp}"