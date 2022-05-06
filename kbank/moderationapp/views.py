import django_filters
from authapp.models import KbankUser
from authapp.permissions import Privileged
from django import forms
from django.db import models
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView
from django_filters import FilterSet
from django_filters.views import FilterView
from mainapp.models import Article, Comment


class ArticleFilter(FilterSet):

    class Meta:
        model = Article
        fields = {
            'title',
            'is_visible',
            'moderation_required',
        }
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }

    def __init__(self, *args, **kwargs):
        super(ArticleFilter, self).__init__(*args, **kwargs)

        for field_name, field in self.form.fields.items():
            field.widget.attrs['class'] = 'm-0'
            field.help_text = ''


class ModerationRequiredArticles(FilterView):
    """
    Контроллер вывода списка статей для модерации
    """
    model = Article
    template_name = 'moderationapp/articles.html'
    context_object_name = 'articles'
    filterset_class = ArticleFilter

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_privileged:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseNotFound('Page not found')


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
