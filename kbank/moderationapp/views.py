from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseNotFound

from django.views.generic import ListView

from mainapp.models import Article, Comment
from authapp.models import KbankUser

from mainapp.views import ArticlesListView
from authapp.permissions import PrivilegedPermissionMixin


class ModerationRequiredArticles(PrivilegedPermissionMixin, ArticlesListView):
    template_name = 'moderationapp/articles.html'

    def get_queryset(self):
        return Article.objects.filter(moderation_required=True).order_by('-publish_date')


class CommentsListView(PrivilegedPermissionMixin, ListView):
    model = Comment
    template_name = 'moderationapp/comments.html'
    context_object_name = 'comments'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CommentsListView, self).get_context_data()
        return context

    def get_queryset(self):
        return Comment.objects.filter(moderation_required=True).order_by('-publish_date')


class UsersListView(PrivilegedPermissionMixin, ListView):
    model = KbankUser
    template_name = 'moderationapp/users.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersListView, self).get_context_data()
        return context

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_privileged:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseNotFound('Page not found')

    def get_queryset(self):
        return KbankUser.objects.filter(moderation_required=True)
