from django.contrib import admin
from . models import Server
# Register your models here.

class ServerAdmin (admin.ModelAdmin):
    list_display = ['id','name','email','password','customDate']

admin.site.register(Server , ServerAdmin)