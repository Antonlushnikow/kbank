from django import forms
from django.forms.widgets import HiddenInput

from .models import Article, Comment


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

    def __init__(self, *args, **kwargs):
        super(ArticleCreateForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ArticleEditForm(forms.ModelForm):
    # Форма изменения статьи
    class Meta:
        model = Article
        fields = [
            'title',
            'category',
            'text',
        ]

    def __init__(self, *args, **kwargs):
        super(ArticleEditForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class CommentForm(forms.ModelForm):
    # Форма добавления комментария
    class Meta:
        model = Comment
        fields = [
            'body',
            'author',
            'article',
        ]
        widgets = {
            'author': HiddenInput,
            'article': HiddenInput,
            'body': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'addANote',
                'placeholder': 'Ваш комментарий...',
            })
        }
        labels = {
            'body': '',
        }
