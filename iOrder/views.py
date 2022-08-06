from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from decimal import Decimal
from iOrder.models import *
from rest_framework import status
import json
from django.db.models import Q
from iOrder.serializers import OrderSerializerAfterQR, MenuSerializer, OrderSerializer, UserSerializerWithToken, AllOrderSerializerForAdmin, PaymentMethodSerializer, OrderSerializerwithTransaction


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Create your views here.
@api_view(['GET'])
def getMenu(request):
    foodCategories = FoodCategory.objects.all()
    serializer = MenuSerializer(foodCategories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def createOrderWithQR(request, qr):
    try:
        splitQr = qr.split("-")
        tableId = splitQr[1]
        table = Table.objects.get(id=tableId)
        if table:
            if table.isReserved:
                return Response({'detail': 'Table is full.'})
            else:
                order = Order.objects.create(table=table)
                table.isReserved = True
                table.save()
                serializer = OrderSerializerAfterQR(order, many=False)
                return Response(serializer.data)
    except:
        return Response({'detail': 'Invalid QR Code'})


@api_view(['GET'])
def getOrderItems(request, code):
    try:
        order = Order.objects.get(orderCode=code)
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
    except:
        return Response({'detail': 'No Order Found'})


@api_view(['POST'])
def addOrderItems(request, code):
    order = Order.objects.get(orderCode=code)
    data = json.loads(request.data)
    orderItems = data['orderItems']
    if order.isActive:
        if orderItems and len(orderItems)==0:
            return Response({'detail':'No Order Items'})
        else:
            # (3) Create orderItem objects and set order to orderItems relationship
            for i in orderItems:
                fooditem = FoodItem.objects.get(id=int(i['fooditem']))
                try:
                    item = OrderItem.objects.get(Q(order=order), Q(food=fooditem))
                    item.quantity += i['qty']
                    item.price += int(i['qty'])*fooditem.price
                    item.save()
                    order.totalPrice += int(i['qty'])*fooditem.price
                    order.save()
                except OrderItem.DoesNotExist:
                    newitem = OrderItem.objects.create(
                        order=order,
                        food=fooditem,
                        name=fooditem.name,
                        quantity = i['qty'],
                        price= int(i['qty'])*fooditem.price,
                    )
                    order.totalPrice += Decimal(newitem.price)
                    order.save()
            return Response({'detail':'Order placed to the kitchen!'})
    else:
        return Response({'detail':'No order found'})


@api_view(['GET'])
def getPaymentMethods(request, code):
    order = Order.objects.get(orderCode=code)
    if order.isActive:
        allMethods = Payment.objects.all()
        serializer = PaymentMethodSerializer(allMethods, many=True)
        return Response(serializer.data)
    else:
        return Response({'detail':'No order found'})


@api_view(['POST'])
def addPayment(request, code):
    order = Order.objects.get(orderCode=code)
    data = request.data
    paymentMethodId = data["paymentMethodId"]
    if order.isActive:
        order.paymentStatus = "Pending"
        order.save()
        Transaction.objects.create(
            order=order,
            payment=Payment.objects.get(id=paymentMethodId),
            amount=order.totalPrice
        )
        serializer = OrderSerializerwithTransaction(order, many=False)
        return Response(serializer.data)
    else:
        return Response({'detail':'No order found'})


@api_view(['GET'])
def verifyPayment(request, code):
    order = Order.objects.get(orderCode=code)
    if order.isActive:
        order.paymentStatus = "Success"
        order.isPaid = True
        order.save()
        serializer = OrderSerializerwithTransaction(order, many=False)
        return Response(serializer.data)
    else:
        return Response({'detail':'No order found'})


@api_view(['GET'])
def closeOrder(request, code):
    order = Order.objects.get(orderCode=code)
    if order.isActive:
        order.isActive = False
        order.table.isReserved = False
        order.save()
        return Response({'detail':''})
    else:
        return Response({'detail':'No order found'})


@api_view(['GET'])
def getAllOrdersForAdmin(request):
    allorders = Order.objects.filter(isActive=True)
    serializer = AllOrderSerializerForAdmin(allorders, many=True)
    return Response(serializer.data)


    # {
    #     "orderItems": [
    #         {
    #             "qty": 2,
    #             "fooditem": 1
    #         },
    #         {
    #             "qty": 2,
    #             "fooditem": 2
    #         }
    #     ]
    # }