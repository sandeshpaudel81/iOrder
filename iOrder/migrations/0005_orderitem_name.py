# Generated by Django 4.0.3 on 2022-08-05 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iOrder', '0004_remove_foodcategory_restaurant_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
