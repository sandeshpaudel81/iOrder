# Generated by Django 4.0.3 on 2022-04-11 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iOrder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderCode',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
