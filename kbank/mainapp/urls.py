from django.urls import path
from .views import ArticleReadView, ArticleEditView, ArticleCreateView

urlpatterns = [
    path('<int:pk>/', ArticleReadView.as_view(), name='article'),
    path('create/', ArticleCreateView.as_view(), name='create-article'),
    path('<int:pk>/edit/', ArticleEditView.as_view(), name='edit-article'),
]
