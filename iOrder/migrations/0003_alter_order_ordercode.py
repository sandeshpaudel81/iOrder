# Generated by Django 4.0.3 on 2022-04-11 18:12

from django.db import migrations, models
import iOrder.models


class Migration(migrations.Migration):

    dependencies = [
        ('iOrder', '0002_alter_order_ordercode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderCode',
            field=models.PositiveIntegerField(blank=True, default=iOrder.models.create_orderCode, null=True, unique=True),
        ),
    ]
