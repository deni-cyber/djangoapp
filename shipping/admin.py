from django.contrib import admin
from .models import County, Town, PickupPoint

admin.site.register(County)
admin.site.register(Town)
admin.site.register(PickupPoint)
