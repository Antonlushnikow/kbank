from django.shortcuts import render
from django.views.generic import ListView

from mainapp.models import Article


class ArticlesListView(ListView):
    model = Article
    template_name = 'mainapp/index.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticlesListView, self).get_context_data()
        context['title'] = 'Статьи участников'

        return context

    def get_queryset(self):
        return Article.objects.all()
