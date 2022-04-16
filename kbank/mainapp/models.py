from django.db import models
from django.conf import settings
from tinymce.models import HTMLField


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок')
    text = HTMLField(verbose_name='текст')
    publish_date = models.DateField(auto_now_add=True, verbose_name='дата публикации')
    updated_date = models.DateField(auto_now=True, verbose_name='дата изменения')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='автор'
    )

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
