# Generated by Django 5.0.6 on 2024-08-16 12:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0024_orders_order_fcm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kitchenspeciality',
            name='Kitchen',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kitchen_specialities', to='webApp.kitchen'),
        ),
    ]
