from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from mainapp.views import ArticlesListView, CategoryListView
from authapp.views import ProfileView
from moderationapp.views import ModerationRequiredArticles, CommentsListView, UsersListView

urlpatterns = [
    path('articles/', ModerationRequiredArticles.as_view(), name='moderate-articles'),
    path('comments/', CommentsListView.as_view(), name='moderate-comments'),
    path('users/', UsersListView.as_view(), name='moderate-users'),
]
