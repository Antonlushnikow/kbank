from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from authapp.views import ProfileView
from mainapp.views import ArticlesListView, CategoryListView
from moderationapp.views import (
    ArticleModerationPassed,
    ArticleModerationRequired,
    ArticleVisibleToggle,
    CommentModerationChecked,
    CommentsListView,
    CommentVisibleToggle,
    ModerationRequiredArticles,
    UserModerationChecked,
    UsersListView,
)

urlpatterns = [
    path("articles/", ModerationRequiredArticles.as_view(), name="moderate-articles"),
    path("comments/", CommentsListView.as_view(), name="moderate-comments"),
    path("users/", UsersListView.as_view(), name="moderate-users"),
    path(
        "article/<int:pk>/hide/",
        ArticleVisibleToggle.as_view(),
        name="article-visible-toggle",
    ),
    path(
        "article/<int:pk>/moderate-required/",
        ArticleModerationRequired.as_view(),
        name="set-moderation-required",
    ),
    path(
        "article/<int:pk>/moderation-passed/",
        ArticleModerationPassed.as_view(),
        name="set-moderation-passed",
    ),
    path(
        "comment/<int:pk>/hide/",
        CommentVisibleToggle.as_view(),
        name="comment-visible-toggle",
    ),
    path(
        "user/<int:pk>/checked/", UserModerationChecked.as_view(), name="user-checked"
    ),
    path(
        "comment/<int:pk>/checked/",
        CommentModerationChecked.as_view(),
        name="comment-checked",
    ),
]
