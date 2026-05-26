from django.contrib import admin
from .models import Post, Like, Comment, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["user", "text", "created_at"]
    list_filter = ["created_at"]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "created_at"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "text", "created_at"]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ["follower", "following", "created_at"]
