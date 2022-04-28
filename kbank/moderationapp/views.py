from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from mainapp.models import Article, Comment
from authapp.models import KbankUser

from mainapp.views import ArticlesListView


class ModerationRequiredArticles(ArticlesListView):
    template_name = 'moderationapp/articles.html'

    def get_queryset(self):
        return Article.objects.filter(moderation_required=True).order_by('-publish_date')


class CommentsListView(ListView):
    model = Comment
    template_name = 'moderationapp/comments.html'
    context_object_name = 'comments'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CommentsListView, self).get_context_data()
        return context

    def get_queryset(self):
        return Comment.objects.filter(moderation_required=True).order_by('-publish_date')


class UsersListView(ListView):
    model = KbankUser
    template_name = 'moderationapp/users.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersListView, self).get_context_data()
        return context

    def get_queryset(self):
        return KbankUser.objects.filter(moderation_required=True)
