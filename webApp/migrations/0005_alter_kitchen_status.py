# Generated by Django 5.0.6 on 2024-07-02 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0004_kitchen_kitchenaddress_kitchenmedia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kitchen',
            name='status',
            field=models.CharField(default='pending', max_length=522),
        ),
    ]