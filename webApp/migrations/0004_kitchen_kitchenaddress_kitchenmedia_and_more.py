# Generated by Django 5.0.6 on 2024-07-02 07:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0003_alter_menuitems_subdivision'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kitchen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=522)),
                ('owner', models.CharField(max_length=522)),
                ('contact', models.CharField(max_length=522)),
                ('email', models.EmailField(max_length=254)),
                ('status', models.CharField(max_length=522)),
            ],
        ),
        migrations.CreateModel(
            name='KitchenAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line1', models.CharField(max_length=122, null=True)),
                ('address_line2', models.CharField(max_length=122, null=True)),
                ('city', models.CharField(max_length=122, null=True)),
                ('country', models.CharField(max_length=122, null=True)),
                ('postal_code', models.CharField(max_length=122, null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('Kitchen', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='webApp.kitchen')),
            ],
        ),
        migrations.CreateModel(
            name='KitchenMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='static/kitchen_media')),
                ('Kitchen', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webApp.kitchen')),
            ],
        ),
        migrations.CreateModel(
            name='KitchenSpeciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.TextField(default='[]')),
                ('Kitchen', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='webApp.kitchen')),
            ],
        ),
        migrations.DeleteModel(
            name='UsersSuggestions',
        ),
    ]
