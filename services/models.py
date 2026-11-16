from django.db import models

class ServiceType(models.Model):
    service_type_ID = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=100)

    def __str__(self):
        return self.service_name
