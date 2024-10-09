from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    created = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


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
    created = models.DateField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateField(auto_now=True)
    pub_date = models.DateField(default=timezone.now())

    objects = ModelManager()

    class Meta:
        ordering = ('created',)
        verbose_name = 'پوست'
        verbose_name_plural = 'پوست ها'

    def get_absolute_url(self):
        return reverse('blog:post_details', kwargs={'pk': self.pk})

    def show_image(self):
        return format_html(f'<img src="{self.image.url}" width="12%" alt="تصویر ندارد"/>')
    show_image.short_description = 'تصویر'

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

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'


class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'
