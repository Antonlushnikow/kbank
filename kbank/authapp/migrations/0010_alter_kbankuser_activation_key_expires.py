# Generated by Django 4.0.3 on 2022-04-26 19:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0009_merge_20220425_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kbankuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 27, 19, 45, 39, 720624, tzinfo=utc)),
        ),
    ]
