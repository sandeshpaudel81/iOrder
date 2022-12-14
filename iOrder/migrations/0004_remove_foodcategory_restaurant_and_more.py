# Generated by Django 4.0.3 on 2022-08-05 08:58

from django.db import migrations, models
import django.db.models.deletion
import iOrder.models


class Migration(migrations.Migration):

    dependencies = [
        ('iOrder', '0003_alter_order_ordercode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodcategory',
            name='restaurant',
        ),
        migrations.RemoveField(
            model_name='fooditem',
            name='restaurant',
        ),
        migrations.RemoveField(
            model_name='order',
            name='restaurant',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='restaurant',
        ),
        migrations.RemoveField(
            model_name='table',
            name='restaurant',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='restaurant',
        ),
        migrations.AlterField(
            model_name='order',
            name='orderCode',
            field=models.PositiveIntegerField(default=iOrder.models.create_orderCode, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='table',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='iOrder.table'),
        ),
        migrations.DeleteModel(
            name='Restaurant',
        ),
    ]
