from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_line = models.CharField(max_length=255)
    county = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
