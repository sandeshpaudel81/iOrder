from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from decimal import Decimal
from iOrder.models import *
from rest_framework import status

from iOrder.serializers import OrderSerializerAfterQR, MenuSerializer, OrderSerializer, UserSerializerWithToken, AllOrderSerializerForAdmin


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
    order = Order.objects.get(orderCode=code)
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def addOrderItems(request, code):
    order = Order.objects.get(orderCode=code)
    data = request.data
    orderItems = data['orderItems']
    if order.isActive:
        if orderItems and len(orderItems)==0:
            return Response({'detail':'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # (3) Create orderItem objects and set order to orderItems relationship
            for i in orderItems:
                fooditem = FoodItem.objects.get(id=i['fooditem'])
                item = OrderItem.objects.create(
                    order=order,
                    food=fooditem,
                    name=fooditem.name,
                    quantity = i['qty'],
                    price= i['price'],
                )
                order.totalPrice += Decimal(i['price'])
                order.save()
                # (4) Update countInStock of product
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
    else:
        return Response({'detail':'No order found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getAllOrdersForAdmin(request):
    allorders = Order.objects.filter(isActive=True)
    serializer = AllOrderSerializerForAdmin(allorders, many=True)
    return Response(serializer.data)