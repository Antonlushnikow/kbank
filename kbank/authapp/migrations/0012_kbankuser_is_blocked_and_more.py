# Generated by Django 4.0.3 on 2022-04-28 16:48

import authapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0011_remove_kbankuser_is_blocked_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='kbankuser',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='kbankuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=authapp.models.default_key_expires),
        ),
    ]
