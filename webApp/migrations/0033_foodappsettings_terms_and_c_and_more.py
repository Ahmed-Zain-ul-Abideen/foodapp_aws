# Generated by Django 5.0.6 on 2024-09-03 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0032_orders_is_cod'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodappsettings',
            name='terms_and_c',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='paymentaccounts',
            name='bank_name',
            field=models.CharField(max_length=522, null=True),
        ),
    ]
