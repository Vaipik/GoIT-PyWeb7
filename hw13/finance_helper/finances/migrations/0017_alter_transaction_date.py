# Generated by Django 4.1.4 on 2022-12-30 08:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0016_alter_transaction_account_alter_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Date'),
        ),
    ]
