# Generated by Django 5.0.6 on 2024-07-29 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0011_kitchen_kitchen_admin_adminaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminaddress',
            name='address_details',
            field=models.CharField(max_length=522, null=True),
        ),
    ]
