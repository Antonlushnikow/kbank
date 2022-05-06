from django import forms
import django_filters

from mainapp.models import Article


class ArticlesFilterForm(django_filters.FilterSet):
    is_visible = django_filters.BooleanFilter()
    moderation_required = django_filters.BooleanFilter()

    class Meta:
        model = Article
        fields = ['is_visible', 'moderation_required']

    def __init__(self, *args, **kwargs):
        super(ArticlesFilterForm, self).__init__(*args, **kwargs)
