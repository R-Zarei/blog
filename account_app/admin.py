from django.contrib import admin
from .models import Profile

# Register your models here.

admin.site.register(Profile)

admin.site.site_header = 'وبلاگ'
admin.site.index_title = 'مدریت وبلاگ'
