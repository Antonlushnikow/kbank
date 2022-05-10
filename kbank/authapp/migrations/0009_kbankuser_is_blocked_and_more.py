import datetime
from django.db import migrations, models
from django.utils.timezone import utc

import authapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0008_alter_kbankuser_activation_key_expires'),
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
