from django.contrib import admin
from .models import *


# Register your models here.
# 博客
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'content', 'author', 'create_time', 'up')


# 评论
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'created_time', 'up')


admin.site.register(Content, ContentAdmin)
