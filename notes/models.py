from django.db import models
from django.conf import settings

# Create your models here.

class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date = models.DateField()
    note = models.TextField()

    def __str__(self):
        return self.title