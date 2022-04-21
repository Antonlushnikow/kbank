# Generated by Django 4.0.3 on 2022-04-20 14:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0005_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'комментарий', 'verbose_name_plural': 'комментарии'},
        ),
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='article_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
