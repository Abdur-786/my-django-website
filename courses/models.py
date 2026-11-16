from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='courses/images/')
    date = models.DateField()
    description = models.TextField()
    content = models.TextField()
    users_enrolled = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='enrolled_courses', blank=True)

    def __str__(self):
        return self.title