# Generated by Django 5.0.6 on 2024-07-30 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0014_alter_adminaddress_admin_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='kitchenaddress',
            name='address_details',
            field=models.CharField(max_length=522, null=True),
        ),
    ]