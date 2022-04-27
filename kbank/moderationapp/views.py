from django.shortcuts import render

# Create your views here.
from mainapp.models import Article
from mainapp.views import ArticlesListView


class ModerationRequiredArticles(ArticlesListView):
    template_name = 'moderationapp/articles.html'

    def get_queryset(self):
        return Article.objects.filter(moderation_required=True).order_by('-publish_date')
