from django.urls import path
from .views import (
    ArticleReadView,
    ArticleEditView,
    ArticleCreateView,
    ArticleLikeAPIView,
    CommentLikeAPIView,
    ArticleListAuthorView,
    CommentVisibleToggleAPI,
    CommentAPIView,
)

urlpatterns = [
    path('<int:pk>/', ArticleReadView.as_view(), name='article'),
    path('create/', ArticleCreateView.as_view(), name='create-article'),
    path('<int:pk>/edit/', ArticleEditView.as_view(), name='edit-article'),
    path('author/<int:pk>/', ArticleListAuthorView.as_view(), name='list-author-articles'),

    path('api/<int:pk>/like/', ArticleLikeAPIView.as_view(), name='like-api'),
    path('api/comment/<int:pk>/like/', CommentLikeAPIView.as_view(), name='comment-like-api'),

    path('api/comment/<int:pk>/', CommentAPIView.as_view(), name='comment-api'),
    path('api/comment/<int:pk>/hide/', CommentVisibleToggleAPI.as_view(), name='comment-visible-toggle'),
]
