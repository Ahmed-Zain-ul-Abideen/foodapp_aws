# Generated by Django 5.0.6 on 2024-07-30 08:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0013_remove_menu_menu_count_menucategory_menu_count_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminaddress',
            name='admin_address',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_adrress_record', to=settings.AUTH_USER_MODEL),
        ),
    ]
