from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


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

    class Meta:
        ordering = ('created',)

    def get_absolute_url(self):
        return reverse('blog:post_details', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.pk}. {self.title}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    # many to one related to object of this model for replies.
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.post}. {self.user}. {self.body[:50]}'


class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
