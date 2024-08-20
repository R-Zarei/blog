from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique_for_date='pub_date')
    body = models.TextField()
    image = models.ImageField(upload_to='img/post')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    pub_date = models.DateField(default=timezone.now())

    def __str__(self):
        return self.title
