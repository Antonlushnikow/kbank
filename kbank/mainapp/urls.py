from django.urls import path

from .views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleEditView,
    ArticleLikeAPIView,
    ArticleListAuthorView,
    ArticlePinView,
    ArticleReadView,
    CommentAPIView,
    CommentLikeAPIView,
    CommentVisibleToggleAPI,
    NotificationReadToggleAPI,
    NotificationsMarkRead,
    ReportCommentAPI,
    SearchResultsView,
)

urlpatterns = [
    path("<int:pk>/", ArticleReadView.as_view(), name="article"),
    path("create/", ArticleCreateView.as_view(), name="create-article"),
    path("<int:pk>/edit/", ArticleEditView.as_view(), name="edit-article"),
    path("<int:pk>/delete/", ArticleDeleteView.as_view(), name="delete-article"),
    path("<int:pk>/pin/", ArticlePinView.as_view(), name="pin-article"),
    path(
        "author/<int:pk>/", ArticleListAuthorView.as_view(), name="list-author-articles"
    ),
    path("api/<int:pk>/like/", ArticleLikeAPIView.as_view(), name="like-api"),
    path(
        "api/comment/<int:pk>/like/",
        CommentLikeAPIView.as_view(),
        name="comment-like-api",
    ),
    path("api/comment/<int:pk>/", CommentAPIView.as_view(), name="comment-api"),
    path(
        "api/comment/<int:pk>/hide/",
        CommentVisibleToggleAPI.as_view(),
        name="comment-visible-toggle",
    ),
    path(
        "api/comment/<int:pk>/report/",
        ReportCommentAPI.as_view(),
        name="report-comment",
    ),
    path(
        "api/notification/<int:pk>/read/",
        NotificationReadToggleAPI.as_view(),
        name="notification-read-toggle",
    ),
    path("search-results/", SearchResultsView.as_view(), name="search"),
    path(
        "notifications-mark-read/",
        NotificationsMarkRead.as_view(),
        name="notifications-mark-as-read",
    ),
]
