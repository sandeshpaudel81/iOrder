from dataclasses import field, fields
from rest_framework import serializers
from iOrder.models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin']

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin', 'token']
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)



class OrderSerializerAfterQR(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['table', 'orderCode']


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    fooditems = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FoodCategory
        fields = ['id', 'name', 'description', 'fooditems']

    def get_fooditems(self, obj):
        items = obj.fooditem_set.all()
        serializer = FoodItemSerializer(items, many=True)
        return serializer.data


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField(read_only=True)
    table_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'table', 'table_name', 'orderCode', 'totalPrice', 'createdAt', 'isPaid', 'isAllDelivered', 'items']

    def get_items(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_table_name(self, obj):
        return obj.table.name


class AllOrderSerializerForAdmin(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class OrderSerializerwithTransaction(OrderSerializer):
    transaction = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'table', 'table_name', 'orderCode', 'totalPrice', 'createdAt', 'isPaid', 'isAllDelivered', 'paymentStatus', 'items', 'transaction']

    def get_transaction(self, obj):
        transaction = Transaction.objects.get(order=obj)
        serializer = TransactionSerializer(transaction, many=False)
        return serializer.data