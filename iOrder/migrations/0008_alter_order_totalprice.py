# Generated by Django 4.0.3 on 2022-08-06 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iOrder', '0007_remove_order_payment_order_paymentstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='totalPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
