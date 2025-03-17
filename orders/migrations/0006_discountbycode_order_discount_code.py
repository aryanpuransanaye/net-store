# Generated by Django 5.1.6 on 2025-03-17 14:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_remove_orderitem_image_alter_order_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountByCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_code', models.CharField(max_length=50, unique=True)),
                ('discount_percentage', models.FloatField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('max_usage', models.IntegerField(default=1)),
                ('used_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='discount_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.discountbycode'),
        ),
    ]
