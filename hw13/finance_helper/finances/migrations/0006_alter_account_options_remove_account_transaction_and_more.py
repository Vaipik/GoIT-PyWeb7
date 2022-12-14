# Generated by Django 4.1.4 on 2022-12-23 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0005_account_name_remove_account_transaction_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['-name', '-balance'], 'verbose_name': ('Account',), 'verbose_name_plural': 'Accounts'},
        ),
        migrations.RemoveField(
            model_name='account',
            name='transaction',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='user',
        ),
        migrations.AddField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='finances.account'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Remaining balance'),
        ),
    ]
