# Generated by Django 5.1.6 on 2025-03-17 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_alter_discountbycode_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discountbycode',
            old_name='product',
            new_name='order',
        ),
    ]
