from django.db import models
from django.utils import timezone

class Court(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    customer_name = models.CharField(max_length=100)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    booking_date = models.DateField()
    start_time = models.TimeField()
    duration = models.IntegerField(help_text="Duration in hours")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=15)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-booking_date', '-start_time']

    def __str__(self):
        return f"{self.customer_name} - {self.court.name} - {self.booking_date}"

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.court.price_per_hour * self.duration
        super().save(*args, **kwargs)
