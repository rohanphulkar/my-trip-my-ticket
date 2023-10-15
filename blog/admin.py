from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    exclude = ('slug',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ( 'user','text', 'created_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)