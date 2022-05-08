from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from mainapp.views import ArticlesListView, CategoryListView
from authapp.views import ProfileView
from moderationapp.views import (
    ModerationRequiredArticles,
    CommentsListView,
    UsersListView,
    ArticleVisibleToggle,
    CommentVisibleToggle,
    UserModerationChecked,
    CommentModerationChecked,
    )

urlpatterns = [
    path('articles/', ModerationRequiredArticles.as_view(), name='moderate-articles'),
    path('comments/', CommentsListView.as_view(), name='moderate-comments'),
    path('users/', UsersListView.as_view(), name='moderate-users'),
    path('article/<int:pk>/hide/', ArticleVisibleToggle.as_view(), name='article-visible-toggle'),
    path('comment/<int:pk>/hide/', CommentVisibleToggle.as_view(), name='comment-visible-toggle'),
    path('user/<int:pk>/checked/', UserModerationChecked.as_view(), name='user-checked'),
    path('comment/<int:pk>/checked/', CommentModerationChecked.as_view(), name='comment-checked'),
]
