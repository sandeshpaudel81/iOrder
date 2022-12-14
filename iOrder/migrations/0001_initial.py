# Generated by Django 4.0.3 on 2022-04-11 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='iOrder.foodcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderCode', models.PositiveIntegerField(blank=True, max_length=9, null=True)),
                ('totalPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('isActive', models.BooleanField(default=True)),
                ('isPaid', models.BooleanField(default=False)),
                ('isAllDelivered', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(blank=True, max_length=20, null=True)),
                ('information', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('contact', models.CharField(blank=True, max_length=10, null=True)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('isActive', models.BooleanField(default=True)),
                ('isSuspended', models.BooleanField(default=False)),
                ('isTerminated', models.BooleanField(default=False)),
                ('firstStartedAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transactionAt', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='iOrder.order')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='iOrder.payment')),
                ('restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='iOrder.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=10, null=True)),
                ('qrCode', models.CharField(max_length=20)),
                ('tableCapacity', models.PositiveIntegerField(default=2)),
                ('isReserved', models.BooleanField(default=False)),
                ('restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='iOrder.restaurant')),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='iOrder.restaurant'),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('isServed', models.BooleanField(default=False)),
                ('isOrderAccepted', models.BooleanField(default=True)),
                ('rejectMessage', models.TextField(blank=True, null=True)),
                ('isEditable', models.BooleanField(default=True)),
                ('food', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='iOrder.fooditem')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='iOrder.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='iOrder.payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='iOrder.restaurant'),
        ),
        migrations.AddField(
            model_name='order',
            name='table',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='iOrder.table'),
        ),
        migrations.AddField(
            model_name='fooditem',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='iOrder.restaurant'),
        ),
        migrations.AddField(
            model_name='foodcategory',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='iOrder.restaurant'),
        ),
    ]
