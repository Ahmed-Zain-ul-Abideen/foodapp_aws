# Generated by Django 5.0.6 on 2024-11-18 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0062_deals_menu_dicounted_price_menuitems_dicounted_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deals',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='deals',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
    ]