# Generated by Django 5.0.6 on 2024-12-18 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0073_foodappsettings_kitchen_share_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='riderorders',
            name='delivery_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
