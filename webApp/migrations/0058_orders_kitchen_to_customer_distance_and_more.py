# Generated by Django 5.0.6 on 2024-11-07 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0057_orderitems_delivery_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='kitchen_to_customer_distance',
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='riderorders',
            name='delivery_distance',
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
    ]