# Generated by Django 5.1.2 on 2024-10-24 19:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=100)),
                ('tracking_number', models.CharField(blank=True, max_length=100, null=True)),
                ('estimated_delivery', models.DateTimeField()),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shipping', to='orders.order')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=50)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_address', to='orders.order')),
            ],
        ),
    ]
