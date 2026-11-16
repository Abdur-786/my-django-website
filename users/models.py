from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    image = models.ImageField(
        upload_to='profile_images/',
        default='profile_image_default.jpg',
        blank=True,
    )
    about = models.TextField(blank=True, null=True)
    dateOfBirth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username
