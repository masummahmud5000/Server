from . models import Server
from rest_framework import serializers

class Serializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = '__all__'
