from django.contrib import admin
from . models import Server
# Register your models here.
admin.site.register(Server)

class display (Server):
    list_display = ['id','name','email','password']
