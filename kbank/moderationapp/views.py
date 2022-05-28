import django_filters
from authapp.models import KbankUser
from authapp.permissions import Privileged, PrivilegedPermissionMixin
from django import forms
from django.db import models
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView
from django_filters import FilterSet
from django_filters.views import FilterView
from mainapp.models import Article, Comment
from mainapp.utils import PersonalNotification


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
        }

    def __init__(self, *args, **kwargs):
        super(ArticleFilter, self).__init__(*args, **kwargs)

        for field_name, field in self.form.fields.items():
            field.widget.attrs['class'] = 'm-0'
            field.widget.attrs['style'] = 'margin=0px'
            field.help_text = ''


class ModerationRequiredArticles(PrivilegedPermissionMixin, FilterView):
    """
    Контроллер вывода списка статей для модерации
    """
    paginate_by = 10
    model = Article
    template_name = 'moderationapp/articles.html'
    context_object_name = 'articles'
    filterset_class = ArticleFilter

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by('-publish_date')


class CommentFilter(FilterSet):
    class Meta:
        model = Comment
        fields = {
            'body',
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
        }

    def __init__(self, *args, **kwargs):
        super(CommentFilter, self).__init__(*args, **kwargs)

        for field_name, field in self.form.fields.items():
            field.widget.attrs['class'] = 'm-0'
            field.widget.attrs['style'] = 'margin=0px'
            field.help_text = ''


class CommentsListView(PrivilegedPermissionMixin, FilterView):
    paginate_by = 10
    model = Comment
    template_name = 'moderationapp/comments.html'
    context_object_name = 'comments'
    filterset_class = CommentFilter

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by('-publish_date')


class UserFilter(FilterSet):
    class Meta:
        model = KbankUser
        fields = {
            'username',
            'first_name',
            'last_name',
            'moderation_required',
        }
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }

    def __init__(self, *args, **kwargs):
        super(UserFilter, self).__init__(*args, **kwargs)

        for field_name, field in self.form.fields.items():
            field.widget.attrs['class'] = 'm-0'
            field.widget.attrs['style'] = 'margin=0px'
            field.help_text = ''


class UsersListView(PrivilegedPermissionMixin, FilterView):
    paginate_by = 10
    model = KbankUser
    template_name = 'moderationapp/users.html'
    context_object_name = 'users'
    filterset_class = UserFilter


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


class CommentVisibleToggle(View):
    """
    Показ/скрытие комментария
    """
    model = Comment
    permission_classes = [Privileged]

    def get(self, request, pk=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        obj.is_visible = not obj.is_visible
        obj.moderation_required = False
        obj.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class UserModerationChecked(View):
    """
    Пользователь прошел модерацию
    """
    model = KbankUser
    permission_classes = [Privileged]

    def get(self, request, pk=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        obj.moderation_required = False
        obj.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class CommentModerationChecked(View):
    """
    Комментарий прошел модерацию
    """
    model = Comment
    permission_classes = [Privileged]

    def get(self, request, pk=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        obj.moderation_required = False
        obj.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class ArticleModerationRequired(View):
    """
    Set moderation required for Article
    """
    model = Article
    permission_classes = [Privileged]

    def get(self, request, pk=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        obj.moderation_required = True
        obj.save()
        PersonalNotification(request=request, body="Ваша статья отправлена на модерацию",
                             title='модерация', url=f'/article/{pk}/', users_group=[obj.author]).create()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class ArticleModerationPassed(View):
    """
    Set moderation passed for Article
    """
    model = Article
    permission_classes = [Privileged]

    def get(self, request, pk=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        obj.moderation_required = False
        obj.save()
        PersonalNotification(request=request, body="Ваша статья прошла модерацию и опубликована!",
                             title='модерация', url=f'/article/{pk}/',
                             users_group=[obj.author]).create()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
