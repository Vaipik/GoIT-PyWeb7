# Generated by Django 4.1.4 on 2022-12-23 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0008_account_slug_alter_transaction_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, verbose_name='Remaining balance'),
        ),
    ]
