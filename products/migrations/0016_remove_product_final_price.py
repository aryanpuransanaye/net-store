# Generated by Django 5.1.6 on 2025-03-16 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_brand_image_alter_category_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='final_price',
        ),
    ]
