from . models import Server, Transaction
from rest_framework import serializers
from django.db import transaction
from django.db.models import F
from .models import Transaction
from decimal import Decimal
# /////////////////////////////////////////////////////////
class registerSerializer(serializers.Serializer):

    name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, value):
        alredy = Server.objects.filter(username=value)
        if alredy.exists():
            raise serializers.ValidationError('userAlready')
        elif len(value) < 8:
            raise serializers.ValidationError('usernameNotStrong')
        
        return value
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('passNotStrong')
        
        return value
    
    def create(self, validate_data):
        user = Server.objects.create_user(**validate_data)
        return user
# ////////////////////////////////////////////////////////
class Serializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = '__all__'

class trSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
# ///////////////////////////////////////////////////////////////////
class DepoSerializer(serializers.Serializer):

    password = serializers.CharField(write_only=True)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate_balance(self, value):
        if value < 50:
            raise serializers.ValidationError('balance_zero')
        elif value > 25000:
            raise serializers.ValidationError('balance_limit')
        # print(value)
        return value

    def validate_password(self, value):
        user = self.context.get('request').user
        
        if not user.check_password(value):
            raise serializers.ValidationError('password')

        return value
    
    def update(self, instanse, validated_data):
        
        balance = validated_data['balance']

        try:
            with transaction.atomic():

                userLock = Server.objects.select_for_update().get(id=instanse.id)
                
                userLock.balance = F('balance') + balance
                userLock.save(update_fields=['balance'])
                userLock.refresh_from_db()

                Transaction.objects.create(
                    user=instanse,
                    name='Deposite',
                    amount=f'{balance:.2f}',
                    status='Receive'
                )
                
                return userLock

        except Exception as e:
            raise serializers.ValidationError({'Error': f'{e} Transation not Valid!'})


# ///////////////////////////////////////////////////////////////////////////////////////
class withSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate(self, attrs):
        user = self.context.get('request').user
        balance = attrs['balance']
        password = attrs['password']

        charge = (balance / 1000) * Decimal(7.70)
        charge_balance = balance + charge

        if not user.check_password(password):
            raise serializers.ValidationError('password')
        elif user.balance < charge_balance:
            raise serializers.ValidationError('balance_low')
        elif balance < 50:
            raise serializers.ValidationError('balance_zero')
        elif balance > 25000:
            raise serializers.ValidationError('balance_limit')
        
        attrs['cb'] = charge_balance
        attrs['charge'] = charge
        
        return attrs
    
    def update(self, instance, validated_data):
        
        charge_balance = validated_data['cb']
        charge = validated_data['charge']
        balance = validated_data['balance']
        # print(f'{charge:.2f}')
        # print(f'{balance:.2f}')
        

        try:
            with transaction.atomic():

                userLock = Server.objects.select_for_update().get(id=instance.id)
                userLock.balance = F('balance') - charge_balance
                userLock.save(update_fields=['balance'])
                userLock.refresh_from_db()

                Transaction.objects.create(
                    user=instance,
                    name='Withdraw',
                    amount=f'{balance:.2f}',
                    charge=f'{charge:.2f}',
                    status='Send'
                )
                
                return userLock
                
        except Exception as e:
            raise serializers.ValidationError({'Error': f'{e} Transation not Valid!'})
            # raise serializers.ValidationError({'Error': f'{e} Transation not Valid!'})

# //////////////////////////////////////////////////////////////////////////////////////////////
class sendSerializer(serializers.Serializer):

    userId = serializers.CharField()
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context.get('request').user
        password = attrs['password']
        balance = attrs['balance']
        receiver = attrs['userId']

        charge = Decimal('4.50')
        charge_balance = charge + balance

        receiver_filter = Server.objects.filter(username=receiver)
        receiver_out = receiver_filter.first()
        
        if not user.check_password(password):
            raise serializers.ValidationError('password')
        elif not receiver_filter.exists():
            raise serializers.ValidationError('receiver')
        elif user.username == receiver:
            raise serializers.ValidationError('self')
        elif user.balance < charge_balance:
            raise serializers.ValidationError('balance_low')
        elif balance < 50:
            raise serializers.ValidationError('balance_zoro')
        elif balance > 20000:
            raise serializers.ValidationError('balance_limit')
        
        attrs['charge'] = charge
        attrs['charge_balance'] = charge_balance
        # print(receiver_out)
        attrs['receiver'] = receiver_out
        # print(attrs)
        return attrs
    
    def update(self, instance, validated_data):

        receiver = validated_data['receiver']
        charge = validated_data['charge']
        charge_balance = validated_data['charge_balance']
        balance = validated_data['balance']
        # print(receiver)
        try:
            with transaction.atomic():
                userLock = Server.objects.select_for_update().get(id=instance.id)
                userLock.balance = F('balance') - charge_balance
                userLock.save(update_fields=['balance'])

                # userLock.refresh_from_db()
                userLock.refresh_from_db()

                receiverLock = Server.objects.select_for_update().get(id=receiver.id)            
                receiverLock.balance = F('balance') + balance
                receiverLock.save(update_fields=['balance'])

                receiverLock.refresh_from_db()

                Transaction.objects.create(
                    user=instance,
                    name='Send Money',
                    amount=f'{balance:.2f}',
                    charge=f'{charge:.2f}',
                    status='Send'
                )
                Transaction.objects.create(
                    user=receiver,
                    name='Send Money',
                    amount=f'{balance:.2f}',
                    status='Receive'
                )


                return userLock, receiverLock                

        except Exception as e:
            raise serializers.ValidationError({'Error': f'{e} Transation not Valid!'})
