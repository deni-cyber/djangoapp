from django.db import models

class County(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Town(models.Model):
    name = models.CharField(max_length=100)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='towns')

    class Meta:
        unique_together = ('name', 'county')  # Ensures unique town names per county

    def __str__(self):
        return f"{self.name}, {self.county.name}"


class PickupPoint(models.Model):
    location = models.CharField(max_length=255)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name='pickup_points')
    details = models.TextField(blank=True, null=True)  # Optional additional details

    def __str__(self):
        return f"{self.location} - {self.town.name}, {self.town.county.name}"

class Shipping(models.Model):
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='shipping')
    provider = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    estimated_delivery = models.DateTimeField()
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.SET_NULL, blank=True, null=True, related_name='shipments')
    delivery_type = models.CharField(max_length=20, choices=(('door_delivery', 'Door Delivery'), ('pickup_point', 'Pickup Point')), default='door_delivery')
    address = models.ForeignKey('users.Address', on_delete=models.SET_NULL, blank=True, null=True, related_name='shipments') 

    def __str__(self):
        return f"Shipping for Order {self.order.id} by {self.provider}"
