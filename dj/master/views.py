from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import (TokenError, InvalidToken)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.db import transaction
from django.db.models import F
from .paginations import trPagination
from .serializers import trSerializer, DepoSerializer, Serializer, withSerializer, sendSerializer, registerSerializer

from . models import Server, Transaction

User = get_user_model()
# from django.http import HttpResponse
class register(APIView):
    def post(self, request):
        serial = registerSerializer(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        
#login View Created /////////////////////////////////////////
class loginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            return Response(f'error: user not found', status=status.HTTP_404_NOT_FOUND)
        else:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            
            return Response({
                'access_token' : str(access),
                'refresh_token' : str(refresh)
            }, status=status.HTTP_202_ACCEPTED)

            

class Profile(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        username = user.username.title()
        return Response({
            'username': username,
            'balance': user.balance,
        })
# /////////////////////////////////////////////////////
class transactions(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            querySet = Transaction.objects.filter(user=request.user).order_by("-time")
            serial = trSerializer(querySet, many=True)
            return Response(serial.data)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
#//////////////////////////////////////////////////////
class deposite (APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        serial = DepoSerializer(instance=request.user,data=request.data, context={'request': request})
        if serial.is_valid():
            serial.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        
# ///////////////////////////////////////////////////////////
class withdraw(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serial = withSerializer(instance=request.user, data=request.data, context={'request':request})
        if serial.is_valid():
            serial.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
# //////////////////////////////// Send Money  ////////////////////////////////////////
class sendMoney(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serial = sendSerializer(instance=request.user, data=request.data, context={'request': request})
        if serial.is_valid():
            serial.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
# /////////////////////////////////////////////////////////////////////////////////////