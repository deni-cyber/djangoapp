from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)

    @property
    def email(self):
        return self.user.email
    
    
    def __str__(self) -> str:
        return self.user.username 

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255)
    county = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username 
