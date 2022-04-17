from django import forms

from .models import Article


class ArticleCreateForm(forms.ModelForm):
    # Форма создания статьи
    title = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'size': '60'}))

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
