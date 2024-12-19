# Generated by Django 5.0.6 on 2024-07-23 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0009_kitchen_approved_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitems',
            name='parent_menu',
        ),
        migrations.RemoveField(
            model_name='menuitems',
            name='subdivision',
        ),
        migrations.AddField(
            model_name='menu',
            name='associated_items',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='menu',
            name='menu_count',
            field=models.PositiveIntegerField(default=1),
        ),
    ]