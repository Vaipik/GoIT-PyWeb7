# Generated by Django 4.1.4 on 2022-12-24 09:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0010_transaction_balance_alter_account_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 24, 11, 18, 15, 515654), verbose_name='Date'),
        ),
    ]
