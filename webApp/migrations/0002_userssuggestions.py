# Generated by Django 5.0.6 on 2024-06-04 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersSuggestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=522)),
                ('suggestion', models.TextField()),
            ],
        ),
    ]
