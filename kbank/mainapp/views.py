from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, CreateView, UpdateView, ListView

from .models import Article
from .forms import ArticleCreateForm, ArticleEditForm


class ArticlesListView(ListView):
    model = Article
    template_name = 'mainapp/index.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticlesListView, self).get_context_data()

        return context

    def get_queryset(self):
        return Article.objects.all()


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


class ArticleReadView(DetailView):
    # контроллер вывода статьи по номеру
    model = Article
    template_name = 'mainapp/article.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleReadView, self).get_context_data()
        context['title'] = 'статья'
        return context

    def get_object(self):
        return get_object_or_404(Article, pk=self.kwargs['pk'])


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
        form.instance.author = self.request.user
        item = form.save()
        self.pk = item.pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('articles:article', kwargs={'pk': self.pk})
