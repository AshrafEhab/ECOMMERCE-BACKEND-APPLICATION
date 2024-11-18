from django.utils import timezone
from datetime import timedelta
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .serializers import SignUpSerializer, UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
# Create your views here.

@api_view(['POST']) 
def register(request):
    data = request.data
    user = SignUpSerializer(data=data)

    if not user.is_valid():
        return Response({'details': "username not valid!","error":user.errors}
        )
    else:
        if User.objects.filter(username=data['email']).exists():
            return Response({'details': "username already exists!"},
                    status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            user = User.objects.create(
            first_name  =data['first_name'],
            last_name =data['last_name'],  
            email= data['email'],     
            username= data['email'].split('@')[0],     
            password = make_password(data['password']),
            )
            return Response({'details': "Account Created Successfully"},
                    status = status.HTTP_201_CREATED
            )
        
@api_view(['GET'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated])
def current_user(request):
    user_serializer = UserSerializer(request.user, many = False)
    return Response(user_serializer.data)


@api_view(['POST'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated])
def edit_user(request):
    user = request.user
    data = request.data
    user.first_name  =data['first_name']
    user.last_name =data['last_name']  
    user.email= data['email']     
    user.username= data['email'].split('@')[0] 
    
    if data['password'] != "":
        user.password = make_password(data['password'])
    else:
        pass

    user.save()
    user_serializer = UserSerializer(user, many = False)
    return Response(user_serializer.data)


def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return f"{protocol}://{host}/"

@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User,email=data["email"])
    token = get_random_string(40)
    expire_date = timezone.now()+timedelta(minutes=5)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()

    host = get_current_host(request)
    URL = f"{host}api/reset_password/{token}"
    body = f"Your Password Reset Link: {URL}"
    print(".\n"*30)
    print(f"user:{user}")
    
    send_mail(
        "Password Reset From Ecommerce",
        body,
        "ecommerce@iti.com",
        [data['email']]
    )
    print("already passed") 
    return Response({"details":f"Password sent to {data['email']}"})
    

@api_view(['POST'])
def reset_password(request, token):
    data = request.data
    user = get_object_or_404(User,profile__reset_password_token = token)

    if user.profile.reset_password_expire < timezone.now():
        return Response({"Error":"Token Expired!"},status=status.HTTP_400_BAD_REQUEST)

    if data['password'] != data['confirm_password']:
        return Response({"Error":"Passwords not Matched!"},status=status.HTTP_400_BAD_REQUEST)

    user.password = make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None
    user.profile.save()
    user.save()

    return Response({"Details":"Password Changed Successfully"},status=status.HTTP_202_ACCEPTED)
    
