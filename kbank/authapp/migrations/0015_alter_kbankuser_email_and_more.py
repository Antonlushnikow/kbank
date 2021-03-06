# Generated by Django 4.0.3 on 2022-05-09 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0014_remove_kbankuser_is_blocked_kbankuser_block_expires_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kbankuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='kbankuser',
            name='moderation_required',
            field=models.BooleanField(default=True, verbose_name='Требуется модерация'),
        ),
    ]
