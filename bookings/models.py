from django.db import models
from django.conf import settings
from services.models import ServiceType

class Booking(models.Model):
    booking_ID = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    address = models.CharField(max_length=255, blank=True, null=True)
    reason = models.TextField()

    def __str__(self):
        return f"{self.service_type} booking for {self.user}"
