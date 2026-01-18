# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.exceptions import (TokenError, InvalidToken)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
# from decimal import Decimal
# from django.db import transaction
from rest_framework.generics import ListAPIView
# from django.db.models import F
from .paginations import trPagination
from .serializers import trSerializer, DepoSerializer, Serializer, withSerializer, sendSerializer, registerSerializer, loginSerializer
from .permissions import StaffUser

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
        serial = loginSerializer(data=request.data)
        if serial.is_valid():
            # serial.save()
            return Response(serial.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
# ///////////////////////////////////////////////////////////
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
class transactions(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = trSerializer
    pagination_class = trPagination

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user_id=user.id).order_by('-id')
    

#//////////////////////////////////////////////////////
class deposite (APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,StaffUser]

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