from django import forms

from .models import Article


class ArticleCreateForm(forms.ModelForm):
    # Форма создания статьи
    class Meta:
        model = Article
        fields = [
            'title',
            'category',
            'text',
        ]


class ArticleEditForm(forms.ModelForm):
    # Форма изменения статьи
    class Meta:
        model = Article
        fields = [
            'title',
            'category',
            'text',
        ]
