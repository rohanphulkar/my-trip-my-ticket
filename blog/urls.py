from django.urls import path
from .views import *
urlpatterns = [
    path('posts/', BlogPostList.as_view(), name='post-list'),
    path('posts/<slug:slug>/', BlogPostDetail.as_view(), name='post-detail'),
    path('comments/', CommentView.as_view(), name='comment-list-create'),
]
