# Generated by Django 4.1.4 on 2022-12-26 19:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0014_alter_transaction_balance_alter_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Remaining balance'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 26, 21, 14, 2, 733802), verbose_name='Date'),
        ),
    ]
