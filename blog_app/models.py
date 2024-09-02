from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=100)
    created = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ModelManager(models.Manager):
    def counter(self):
        return len(self.all())

    def published(self):
        return self.first(published=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique_for_date='pub_date')
    category = models.ManyToManyField(Category)
    body = models.TextField()
    image = models.ImageField(upload_to='img/post')
    published = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    pub_date = models.DateField(default=timezone.now())

    objects = ModelManager()

    def __str__(self):
        return self.title
