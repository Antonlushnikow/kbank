from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    ListView,
)
from django.views.generic.edit import FormMixin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .models import Article, Category, Comment
from authapp.models import KbankUser
from .forms import ArticleCreateForm, ArticleEditForm, CommentForm


class ArticlesListView(ListView):
    model = Article
    template_name = 'mainapp/index.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticlesListView, self).get_context_data()
        return context

    def get_queryset(self):
        return Article.objects.all().order_by('-publish_date')


class ArticleCreateView(CreateView):
    # Контроллер создания статьи
    model = Article
    template_name = 'mainapp/create-article.html'
    form_class = ArticleCreateForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/auth/login')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleCreateView, self).get_context_data()
        context['title'] = 'новая статья'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        item = form.save()
        self.pk = item.pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('articles:article', kwargs={'pk': self.pk})


class ArticleReadView(FormMixin, DetailView):
    # контроллер вывода статьи по номеру
    model = Article
    template_name = 'mainapp/article.html'
    form_class = CommentForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleReadView, self).get_context_data()
        context['title'] = 'статья'
        context['form'] = CommentForm(initial={'article': self.object, 'author': self.request.user})
        return context

    def get_object(self):
        return get_object_or_404(Article, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('articles:article', kwargs={'pk': self.object.id})


class ArticleEditView(UpdateView):
    # Контроллер редактирования статьи
    model = Article
    template_name = 'mainapp/edit-article.html'
    form_class = ArticleEditForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleEditView, self).get_context_data()
        context['title'] = 'редактирование статьи'
        return context

    def form_valid(self, form):
        # form.instance.author = self.request.user
        item = form.save()
        self.pk = item.pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('articles:article', kwargs={'pk': self.pk})

    def dispatch(self, request, *args, **kwargs):
        if Article.objects.get(pk=kwargs['pk']).author.id == request.user.id \
                or request.user.is_superuser or request.user.is_moderator:
            return super(ArticleEditView, self).dispatch(request, *args, **kwargs)
        return HttpResponseNotFound('Page not found')


class CategoryListView(ListView):
    # Контроллер вывода статей по категории
    model = Article
    template_name = 'mainapp/index.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data()
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        context['title'] = category.title
        return context

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Article.objects.filter(category=category).order_by('-publish_date')


class ArticleListAuthorView(ListView):
    # Контроллер вывода статей по авторам
    model = Article
    template_name = 'mainapp/index.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleListAuthorView, self).get_context_data()
        author = get_object_or_404(KbankUser, pk=self.kwargs['pk'])
        context['title'] = f'Статьи - {author.username}'
        return context

    def get_queryset(self):
        author = get_object_or_404(KbankUser, pk=self.kwargs['pk'])
        return Article.objects.filter(author=author).order_by('-publish_date')


class LikeAPIView(APIView):
    """
    Представление лайков через API
    Абстрактный класс
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model = None

    def get(self, request, pk=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        user = self.request.user
        updated = False
        liked = False

        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True

        data = {
            'updated': updated,
            'liked': liked,
            'like_count': obj.likes.count(),
        }

        return Response(data)


class ArticleLikeAPIView(LikeAPIView):
    model = Article


class CommentLikeAPIView(LikeAPIView):
    model = Comment
