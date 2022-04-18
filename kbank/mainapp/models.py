from django.db import models
from django.conf import settings
from tinymce.models import HTMLField


class Category(models.Model):
    title = models.CharField(max_length=60, verbose_name='Название категории')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок')
    text = HTMLField(verbose_name='текст')
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='дата изменения')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='автор'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='категория'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
