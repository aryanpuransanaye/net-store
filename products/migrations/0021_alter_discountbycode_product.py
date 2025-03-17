# Generated by Django 5.1.6 on 2025-03-17 14:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_remove_orderitem_image_alter_order_status_and_more'),
        ('products', '0020_product_discount_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountbycode',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order'),
        ),
    ]
