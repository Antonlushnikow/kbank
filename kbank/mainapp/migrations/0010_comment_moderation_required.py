# Generated by Django 4.0.3 on 2022-04-28 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_article_moderation_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='moderation_required',
            field=models.BooleanField(default=True),
        ),
    ]
