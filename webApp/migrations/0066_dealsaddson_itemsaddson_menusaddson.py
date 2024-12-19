# Generated by Django 5.0.6 on 2024-11-21 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0065_remove_orderdealitems_order_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dealsaddson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=522)),
                ('description', models.TextField()),
                ('image', models.FileField(blank=True, max_length=122, null=True, upload_to='static/deals_addson')),
                ('price', models.DecimalField(decimal_places=2, max_digits=15, null=True)),
                ('dicounted_price', models.DecimalField(decimal_places=2, max_digits=15, null=True)),
                ('deal', models.ManyToManyField(related_name='deals_addson_records', to='webApp.deals')),
            ],
        ),
        migrations.CreateModel(
            name='Itemsaddson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=522)),
                ('description', models.TextField()),
                ('image', models.FileField(blank=True, max_length=122, null=True, upload_to='static/items_addson')),
                ('price', models.DecimalField(decimal_places=2, max_digits=15, null=True)),
                ('dicounted_price', models.DecimalField(decimal_places=2, max_digits=15, null=True)),
                ('item', models.ManyToManyField(related_name='items_addson_records', to='webApp.menuitems')),
            ],
        ),
        migrations.CreateModel(
            name='Menusaddson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=522)),
                ('description', models.TextField()),
                ('image', models.FileField(blank=True, max_length=122, null=True, upload_to='static/menus_addson')),
                ('price', models.DecimalField(decimal_places=2, max_digits=15, null=True)),
                ('dicounted_price', models.DecimalField(decimal_places=2, max_digits=15, null=True)),
                ('menu', models.ManyToManyField(related_name='menus_addson_records', to='webApp.menu')),
            ],
        ),
    ]