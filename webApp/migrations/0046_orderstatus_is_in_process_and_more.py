# Generated by Django 5.0.6 on 2024-10-28 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0045_orders_rider_pending'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderstatus',
            name='is_in_process',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderstatus',
            name='is_rider_on_way',
            field=models.BooleanField(default=False),
        ),
    ]