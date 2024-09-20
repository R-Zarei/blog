from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    national_code = models.CharField(max_length=10)
    image = models.ImageField(upload_to='profile/img', blank=True, null=True)

    def __str__(self):
        return self.user.username
