from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .filters import ProductFilter
from .models import Product, Review
from .serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Avg
# Create your views here.
@api_view(['GET']) 
def get_all_products(request):
    # products = Product.objects.all()
    # serializer = ProductSerializer(products, many=True)
    filterset = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id'))
    page_size = 2
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    queryset = paginator.paginate_queryset(filterset.qs,request)
    serializer = ProductSerializer(queryset, many=True)
    count = filterset.qs.count()
    return Response({"Products": serializer.data, "Page: ":f"{paginator.page.number} / {paginator.page.paginator.num_pages}"})

@api_view(['GET']) 
def get_product(request,pk):
    products = get_object_or_404(Product,id=pk)
    serializer = ProductSerializer(products, many=False)
    return Response({"Products": serializer.data})@api_view(['GET']) 

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_product(request):
    data = request.data
    serializer = ProductSerializer(data=data)

    if not serializer.is_valid():
        return Response({"Details":"product not valid","error":data.errors})
    
    else:
        product = Product.objects.create(**data, user=request.user)
        res = ProductSerializer(product, many=False)
        return Response({"Products": res.data})

@api_view(['PUT'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated])
def edit_product(request,pk):
    product = get_object_or_404(Product, id=pk)  

    if product.user != request.user:
        return Response({"ERROR:":"You Have no Access to Edit this Product!."},status=status.HTTP_403_FORBIDDEN)
    
    else:
        product.name = request.data['name']
        product.description = request.data['description']
        product.price = request.data['price']
        product.brand = request.data['brand']
        product.category = request.data['category']
        product.rating = request.data['rating']
        product.stock = request.data['stock']

        #serializer used to update data in db
        product.save()
        serializer = ProductSerializer(product,many=False)
        return Response(serializer.data)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated])
def delete_product(request,pk):
    product = get_object_or_404(Product, id=pk)  

    if product.user != request.user:
        return Response({"ERROR:":"You Have no Access to Delete this Product!."},status=status.HTTP_403_FORBIDDEN)
    
    else:     
        product.delete()
        return Response({"details":"Product Deleted Successfully"},status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_review(request,pk):
    user = request.user
    data = request.data
    product = get_object_or_404(Product,id=pk)
    review = product.reviews.filter(user = user)

    if not 0 <= data['rating'] <= 5:
        return Response({"Error:":"Rating range from 1 to 5"},status=status.HTTP_400_BAD_REQUEST)
    elif review.exists():
        new_review = {'rating':data['rating'],'comment':data['comment']}
        review.update(**new_review)
        rating = product.reviews.aggregate(avg_rating = Avg('rating'))
        product.rating = rating['avg_rating']
        product.save()
        return Response({"Details":"Product Review Edited Successfully"})

    else:
        #printing dots to easly catch in terminal
        # print("...\n"*20)
        # print(f"product = {product},,user = {user},,rating = {data["rating"]},,comment = {data['comment']},,")
        review = Review.objects.create(
            product = product,
            user = user,
            rating  = data['rating'],
            comment = data['comment'],
            )
        rating = product.reviews.aggregate(avg_rating = Avg('rating'))
        product.rating = rating['avg_rating']
        product.save()
        return Response({"Details":"Product Review Created Successfully"},status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated])
def delete_review(request,pk):
    product = get_object_or_404(Product.objects.filter(id=pk))
    review = product.reviews.filter(user = request.user)
    #printing dots to easly catch in terminal
    print("...\n"*20)
    print(review)
    if not review.exists():
        return Response({"ERROR:":"You Have no Access to Delete this Review!."},status=status.HTTP_403_FORBIDDEN)
    
    else:     
        review.delete()
        rating = product.reviews.aggregate(avg_rating = Avg('rating'))
        if rating['avg_rating'] is None:
            rating['avg_rating'] = 0
        else:
            pass
        
        product.rating = rating['avg_rating']
        product.save()
        return Response({"details":"Review Deleted Successfully"},status=status.HTTP_200_OK)
