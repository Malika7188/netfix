from django.db import models
from users.models import Company, Customer

class Service(models.Model):
    FIELD_CHOICES = [
        ('Air Conditioner', 'Air Conditioner'),
        ('Carpentry', 'Carpentry'),
        ('Electricity', 'Electricity'),
        ('Gardening', 'Gardening'),
        ('Home Machines', 'Home Machines'),
        ('Housekeeping', 'Housekeeping'),
        ('Interior Design', 'Interior Design'),
        ('Locks', 'Locks'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing'),
        ('Water Heaters', 'Water Heaters'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    field = models.CharField(max_length=50, choices=FIELD_CHOICES)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.name
    
class RequestedService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='requests')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='requested_services')
    address = models.CharField(max_length=255)
    service_time = models.DecimalField(max_digits=5, decimal_places=2)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    date_requested = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically calculate the total cost based on service time and price per hour
        self.total_cost = self.service.price_per_hour * self.service_time
        super().save(*args, **kwargs)