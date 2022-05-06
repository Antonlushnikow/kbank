from django.http import HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from django.views.generic import ListView
from rest_framework.views import APIView

from authapp.permissions import Privileged
from mainapp.models import Article, Comment
from authapp.models import KbankUser

from mainapp.views import ArticlesListView
from moderationapp.forms import ArticlesFilterForm


class ModerationRequiredArticles(ArticlesListView):
    template_name = 'moderationapp/articles.html'
    form_class = ArticlesFilterForm

    def get(self, request, *args, **kwargs):
        is_visible = request.GET['is_visible']
        moderation_required = request.GET['moderation_required']
        return render(request, self.template_name, context={})

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_privileged:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseNotFound('Page not found')

    def get_queryset(self):
        return Article.objects.filter(moderation_required=True).order_by('-publish_date')


class CommentsListView(ListView):
    model = Comment
    template_name = 'moderationapp/comments.html'
    context_object_name = 'comments'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_privileged:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseNotFound('Page not found')

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

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_privileged:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseNotFound('Page not found')

    def get_queryset(self):
        return KbankUser.objects.filter(moderation_required=True)


class ArticleVisibleToggle(View):
    """
    Показ/скрытие статьи
    """
    model = Article
    permission_classes = [Privileged]

    def get(self, request, pk=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        obj.is_visible = not obj.is_visible
        obj.moderation_required = False
        obj.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
