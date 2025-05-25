from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import Company, Customer


class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=100)
    rating = models.IntegerField(validators=[MinValueValidator(
        0), MaxValueValidator(5)], default=0)
    choices = (
        ('Air Conditioner', 'Air Conditioner'),
        ('Carpentry', 'Carpentry'),
        ('Electricity', 'Electricity'),
        ('Gardening', 'Gardening'),
        ('Home Machines', 'Home Machines'),
        ('House Keeping', 'House Keeping'),
        ('Interior Design', 'Interior Design'),
        ('Locks', 'Locks'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing'),
        ('Water Heaters', 'Water Heaters'),
    )
    field = models.CharField(max_length=30, blank=False,
                             null=False, choices=choices)
    date = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.name


class RequestedService(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    address = models.TextField()
    hours = models.DecimalField(decimal_places=2, max_digits=100)
    date_requested = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(decimal_places=2, max_digits=100)

    def save(self, *args, **kwargs):
        self.total_cost = self.hours * self.service.price_hour
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.user.username} - {self.service.name}"
