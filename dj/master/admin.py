from django.contrib import admin
from . models import Server
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class ServerAdmin (admin.ModelAdmin):
    list_display = ['id','name','username','joinDate','password']

admin.site.register(Server , ServerAdmin)