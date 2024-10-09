from django.contrib import admin
from . import models


class CommentInline(admin.StackedInline):   # can use admin.TabularInline
    model = models.Comment
    extra = 0
    readonly_fields = ('user',)


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created', 'author', 'published', 'show_image')
    list_editable = ('published',)
    list_filter = ('published', 'created')
    search_fields = ('title', 'body')
    # fields = ('title', 'body', 'author', 'published')
    inlines = (CommentInline,)


# admin.site.register(models.Post)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Message)
