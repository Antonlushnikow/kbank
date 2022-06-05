from datetime import datetime, timezone, timedelta

from django.db import models
from django.conf import settings
from django.urls import reverse
from tinymce.models import HTMLField

from .utils import plural_time
from django.utils.timezone import now

from tagulous.models import TagField


class Category(models.Model):
    title = models.CharField(max_length=60, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


TOP_ARTICLE_DURATION_DAYS = 30


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок')
    text = HTMLField(verbose_name='текст')
    preview_text = models.TextField(blank=True, verbose_name='превью')
    source_text = models.CharField(blank=True, max_length=250, verbose_name='текст источника')
    source_url = models.CharField(blank=True, max_length=250, verbose_name='ссылка на источник')
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
    tags = TagField(
        blank=True,
        force_lowercase=True,
        verbose_name='теги (через запятую)',
    )
    views = models.IntegerField(
        default=0,
    )

    moderation_required = models.BooleanField(default=True, verbose_name='Требуется модерация')
    is_visible = models.BooleanField(default=False, verbose_name='Опубликовано')

    pic = models.ImageField(
        upload_to='article_pics/',
        blank=True,
        verbose_name='обложка статьи',
    )

    def __str__(self):
        return self.title

    @property
    def comments_count(self):
        return self.comments.count()

    @property
    def is_last_month(self):
        return now() < self.publish_date + timedelta(days=TOP_ARTICLE_DURATION_DAYS)

    def get_absolute_url(self):
        return reverse('articles:article', args=[str(self.id)])

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"


class Comment(models.Model):
    body = models.TextField(verbose_name='Текст комментария',)
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
    moderation_required = models.BooleanField(default=False, verbose_name='Требуется модерация')

    is_visible = models.BooleanField(default=True, verbose_name='Опубликовано')
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='childs',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.author}: {self.body}'

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"


JUST_NOW = timedelta(minutes=2)  # 2 минуты


class Notification(models.Model):
    title = models.CharField(null=True, max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="notifications",
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    url = models.CharField(default='/', max_length=100)
    is_read = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def time_ago(self):
        now = datetime.now(timezone.utc)
        diff = now - self.created_date

        minutes = int(diff / timedelta(minutes=1))
        hours = int(diff / timedelta(hours=1))

        if diff < JUST_NOW:
            time_ = 'Только что'
        elif diff < timedelta(hours=1):
            time_ = f"{plural_time(minutes, type_='minutes')} назад"
        elif diff < timedelta(days=1):
            time_ = f"{plural_time(hours, type_='hours')} назад"
        else:
            time_ = f"{plural_time(diff.days, type_='days')} назад"
        return time_


class SiteSettings(models.Model):
    about_us = HTMLField(
        blank=True,
        verbose_name='о нас',
    )
    logo_pic = models.ImageField(
        upload_to='site_pics/',
        blank=True,
        default='site_pics/default_logo.png',
        verbose_name='лого сайта',
    )

    pinned_article = models.OneToOneField(
        Article,
        null=True,
        related_name="pinned_article",
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = 'настройки сайта'
        verbose_name_plural = 'настройки сайта'
