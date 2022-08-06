from datetime import timedelta
from unicodedata import decimal
from django.db import models
import random
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import math

# Create your models here.
# class Restaurant(models.Model):
#     name = models.CharField(max_length=300, null=True, blank=True)
#     contact = models.CharField(max_length=10, null=True, blank=True)
#     address = models.CharField(max_length=50, null=True, blank=True)
#     isActive = models.BooleanField(default=True)
#     isSuspended = models.BooleanField(default=False)
#     isTerminated = models.BooleanField(default=False)
#     firstStartedAt = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    
#     def __str__(self):
#         return '%s' % (self.fullName)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Table(models.Model):
    name = models.CharField(max_length=10, null=True, blank=True)
    qrCode = models.CharField(max_length=20)
    tableCapacity = models.PositiveIntegerField(default=2)
    isReserved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.qrCode = 'iOrder-'+str(self.id)
        super(Table, self).save(*args, **kwargs)



class FoodCategory(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Payment(models.Model):
    method = models.CharField(max_length=20, null=True, blank=True)
    information = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.method


def create_orderCode():
    not_unique = True
    while not_unique:
        unique_code = random.randint(100000000, 999999999)
        if not Order.objects.filter(orderCode=unique_code):
            not_unique = False
        return unique_code


class Order(models.Model):
    # restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    orderCode=models.PositiveIntegerField(unique=True, default=create_orderCode)
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    createdAt = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=True)
    isPaid = models.BooleanField(default=False)
    isAllDelivered = models.BooleanField(default=False)
    paymentStatus = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.orderCode)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    food = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isServed = models.BooleanField(default=False)
    isOrderAccepted = models.BooleanField(default=True)
    rejectMessage = models.TextField(null=True, blank=True)
    isEditable = models.BooleanField(default=True)

    def __str__(self):
        return self.food.name

class Transaction(models.Model):
    # restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True,  blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transactionAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transactionAt
