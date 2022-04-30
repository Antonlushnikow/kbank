from django.db import models
from django.conf import settings
from tinymce.models import HTMLField


class Category(models.Model):
    title = models.CharField(max_length=60, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

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
        verbose_name='автор',
        related_name='articles',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='категория'
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='article_likes',
    )

    def __str__(self):
        return self.title

    @property
    def comments_count(self):
        return self.comments.count()

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"


class Comment(models.Model):
    body = models.TextField()
    article = models.ForeignKey(
        Article,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='автор',
        related_name='comments',
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='comment_likes',
    )
    publish_date = models.DateTimeField(auto_now_add=True)

    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.author}: {self.body}'

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"
