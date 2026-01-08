from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import (TokenError, InvalidToken)

from . models import Server
from . serializers import Serializer

# from django.http import HttpResponse
class home(APIView):
    def post(self, request):
        name = request.data.get('name')
        username = request.data.get('username')
        password = request.data.get('password')

        if not name or not username or not password:
            return Response('error : Sob field dite hobe ', status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                if Server.objects.filter(username=username).exists():
                    return Response('user Alredy Created!', status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    user = Server.objects.create_user(
                        username=username,
                        name=name,
                        password=password
                    )
                    return Response('Success: user Create', status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(f'error: {str(e)}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create your views here.
        
#login View Created /////////////////////////////////////////
class loginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            return Response(f'error: user not found, {username} {password}', status=status.HTTP_401_UNAUTHORIZED)
        else:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            return Response({
                'access_token' : str(access),
                'refresh_token' : str(refresh)
            }, status=status.HTTP_202_ACCEPTED)

            
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class Profile(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user

        return Response({
            'username': user.username,
            'balance': user.balance
        })
    
#//////////////////////////////////////////////////////