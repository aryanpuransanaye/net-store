# Generated by Django 5.1.6 on 2025-03-26 23:05

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_rename_discount_precentage_order_discount_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=10, null=True),
        ),
    ]
