from dataclasses import field
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

    class Meta:
        model = Order
        fields = ['id', 'table', 'orderCode', 'totalPrice', 'createdAt', 'isPaid', 'isAllDelivered', 'items']

    def get_items(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data


class AllOrderSerializerForAdmin(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

