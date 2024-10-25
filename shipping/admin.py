from django.contrib import admin
from .models import Shipping, ShippingAddress

admin.site.register(Shipping)
admin.site.register(ShippingAddress)