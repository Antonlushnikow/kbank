# Generated by Django 4.0.3 on 2022-04-27 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_alter_article_author_alter_comment_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='moderation_required',
            field=models.BooleanField(default=True),
        ),
    ]
