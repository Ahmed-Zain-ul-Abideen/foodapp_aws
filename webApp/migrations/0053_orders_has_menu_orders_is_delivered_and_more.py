# Generated by Django 5.0.6 on 2024-11-05 12:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0052_orders_order_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='has_menu',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orders',
            name='is_delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orders',
            name='kitchen_pickup_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='max_deliverable',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.CreateModel(
            name='MenuFoodRecords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(null=True)),
                ('delivery_date', models.DateField()),
                ('item', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='menu_order_item', to='webApp.menuitems')),
                ('menu', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='menu_related_food', to='webApp.menu')),
                ('order', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='order_menu_food', to='webApp.orders')),
            ],
        ),
    ]
