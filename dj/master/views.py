from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . models import Server
from . serializers import Serializer
# from django.http import HttpResponse

# Create your views here.
class home(APIView):
    def get(self, request, pk=None):
        try:
            querySet = Server.objects.all()
            serial = Serializer(querySet, many=True)
            return Response(serial.data)

        except Server.DoesNotExist:
            return Response('Masum Software Foundation',status=status.HTTP_404_NOT_FOUND)