from . models import Server, Transaction
from rest_framework import serializers
from django.db import transaction
from django.db.models import F

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
        if value <= 0 or value < 50:
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
                instanse.balance = F('balance') + balance
                instanse.save()

                # instanse.refresh_from_db()
                return instanse

                
        except Exception as e:
            raise serializers.ValidationError({'Error': f'{e} Transation not Valid!'})