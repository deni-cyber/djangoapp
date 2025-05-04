from django.contrib import admin
from .models import Payment, PaymentCallbackLog

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'amount', 'status', 'receipt_number', 'phone_number', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'order__id', 'receipt_number', 'phone_number')

@admin.register(PaymentCallbackLog)
class PaymentCallbackLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'processed')
    list_filter = ('processed',)
    search_fields = ('raw_data',)
