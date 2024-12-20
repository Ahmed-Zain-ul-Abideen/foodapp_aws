# Generated by Django 5.0.6 on 2024-07-29 09:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0010_remove_menuitems_parent_menu_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='kitchen',
            name='kitchen_admin',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.CreateModel(
            name='AdminAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line1', models.CharField(max_length=122, null=True)),
                ('address_line2', models.CharField(max_length=122, null=True)),
                ('city', models.CharField(max_length=122, null=True)),
                ('country', models.CharField(max_length=122, null=True)),
                ('postal_code', models.CharField(max_length=122, null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('admin_address', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
