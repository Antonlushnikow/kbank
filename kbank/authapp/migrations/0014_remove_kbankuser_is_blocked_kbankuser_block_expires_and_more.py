# Generated by Django 4.0.3 on 2022-05-03 14:21

import datetime
from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0013_merge_20220502_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kbankuser',
            name='is_blocked',
        ),
        migrations.AddField(
            model_name='kbankuser',
            name='block_expires',
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0)),
        ),
        migrations.AlterField(
            model_name='kbankuser',
            name='avatar',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], default='users_avatar/default.png', force_format=None, keep_meta=True, quality=0, size=[300, 300], upload_to='users_avatar/', verbose_name='аватар'),
        ),
    ]
