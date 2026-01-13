from . models import Server, Transaction
from rest_framework import serializers

class Serializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = '__all__'

class trSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'