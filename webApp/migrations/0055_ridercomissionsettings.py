# Generated by Django 5.0.6 on 2024-11-06 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0054_orderprocessedstatuses_processed_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='RiderComissionsettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('by_distance', models.PositiveIntegerField(default=1)),
                ('amount_share', models.PositiveIntegerField(default=100)),
            ],
        ),
    ]