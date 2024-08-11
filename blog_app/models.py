from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    body = models.TextField()
    image = models.ImageField(upload_to='img/post')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
