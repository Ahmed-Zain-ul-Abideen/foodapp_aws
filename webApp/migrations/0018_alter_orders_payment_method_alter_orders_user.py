# Generated by Django 5.0.6 on 2024-08-01 13:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0017_orderaddson_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='payment_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webApp.paymentmethods'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='user',
            field=models.CharField(max_length=522, null=True),
        ),
    ]
