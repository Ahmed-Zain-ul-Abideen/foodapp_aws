# Generated by Django 5.0.6 on 2024-10-25 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0043_riderdetails_device_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitems',
            name='exclusive',
            field=models.BooleanField(default=False),
        ),
    ]
