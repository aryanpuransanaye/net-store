# Generated by Django 5.1.6 on 2025-03-16 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_remove_product_final_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='final_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
