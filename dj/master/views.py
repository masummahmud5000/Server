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

from . models import Server, Transaction
from . serializers import Serializer

User = get_user_model()
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
            'balance': user.balance
        })
    
#//////////////////////////////////////////////////////
class deposite (APIView):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        try:
            balance = Decimal(request.data.get('balance', 0))
            password = request.data.get('password')

            user = request.user
            if not user.check_password(password):
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                if balance <= 0:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                else:
                    user.balance = F('balance') + balance
                    user.save()

                    Transaction.objects.create(
                        user=user,
                        name='Deposite',
                        amount=balance,
                        status='Successfull',
                    )
                    
                    return Response(status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# ///////////////////////////////////////////////////////////
class withdraw(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):

        balance = Decimal(request.data.get('balance'))
        password = request.data.get('password')
        charge = (balance / 1000) * Decimal(7.70)
        update_charge = Decimal(charge + balance)

        try:
            user = request.user
            admin = User.objects.filter(username='admin').first()

            if not user.check_password(password):
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                if user.balance < update_charge or update_charge <= 0:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                else:
                    user.balance = F('balance') - update_charge
                    user.save()
                    admin.balance = F('balance') + update_charge
                    admin.save()
                    
                    charge_history = f"{charge:.2f}"
                    Transaction.objects.create(
                        user=user,
                        name='Withdraw',
                        amount=str(balance),
                        charge=str(charge_history),
                        status='Send'
                    )
                    # print(admin.id)
                    # print(charge_history, type(charge_history))
                    Transaction.objects.create(
                        user=admin,
                        name='Withdraw',
                        amount=f'{update_charge:.2f}',
                        status='Receive'
                    )
                    # print(admin.id)

                    return Response(status=status.HTTP_202_ACCEPTED)
                # ////////////////////////
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# //////////////////////////////// Send Money  ////////////////////////////////////////
class sendMoney(APIView):
    @transaction.atomic
    def post(self, request):
        userId = request.data.get('userId')
        balance = Decimal(request.data.get('balance'))
        password = request.data.get('password')

        myObjects = request.user

        try:
            receiver = User.objects.filter(username=userId)
            charge = Decimal(4.50)
            charge_update = Decimal(balance + charge)

            if not myObjects.check_password(password):
                return Response({'Error':'password'})
            else:
                if not receiver.exists():
                    return Response({'Error': 'userName'})
                else:
                    if myObjects.username == userId:
                        return Response({'Error': 'self'})
                    else:
                        if myObjects.balance < charge_update or balance <= 0:
                            return Response({'Error': 'balance'})
                        else:
                            receiver_update = receiver.first()

                            myObjects.balance = F('balance') - charge_update
                            myObjects.save()

                            receiver_update.balance = F('balance') + balance
                            receiver_update.save()

                            return Response({'Error': 'success'})
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
