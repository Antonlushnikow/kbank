import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0009_kbankuser_is_blocked_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kbankuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 28, 16, 38, 32, 998339, tzinfo=utc)),
        ),
    ]
