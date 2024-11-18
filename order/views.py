from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from product.models import Product
from .models import Order, OrderItem
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Avg
from .serializers import OrderSerializer
# Create your views here.

@api_view(['POST'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated])

def new_order(request):
    user = request.user
    data = request.data
    order_items = data['order_items']
    if len(order_items) == 0:
        return Response({"Error": "No or Order Items Found"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        total_price = sum(Product.objects.get(id = item['product']).price * item['quantity'] for item in order_items)
        order = Order.objects.create(
            user = user,
            city = data['city'],
            zip_code = data['zip_code'],
            street = data['street'],
            country = data['country'],
            phone_no = data['phone_no'],
            total_price = total_price,
        )
        for order_item in order_items:
            product = Product.objects.get(id = order_item['product'])
            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,
                quantity = order_item['quantity'],
                price = product.price
            )
            product.stock -= order_item['quantity']
            product.save()
    

        serializer = OrderSerializer(order,many=False)
        return Response(serializer.data)



@api_view(['GET'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated])

def get_all_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response({"Orders:":serializer.data})



@api_view(['GET'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated])

def get_order_by_id(request,pk):
    order = get_object_or_404(Order,id=pk)
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)



@api_view(['PUT'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated, IsAdminUser])

def edit_order_status_by_id(request,pk):
    order = get_object_or_404(Order,id=pk)
    order.status = request.data['status']
    order.save()
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated, IsAdminUser])

def delete_order_by_id(request,pk):
    order = get_object_or_404(Order,id=pk)
    order.delete()
    return Response({"details:":"Deleted Successfully"})
