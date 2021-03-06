# Generated by Django 4.0.3 on 2022-04-23 05:15

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_kbankuser_is_moderator_alter_kbankuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kbankuser',
            name='avatar',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], default='/users_avatar/default.png', force_format=None, keep_meta=True, quality=0, size=[300, 300], upload_to='users_avatar/', verbose_name='аватар'),
        ),
    ]
