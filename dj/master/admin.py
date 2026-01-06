from django.contrib import admin
from . models import Server
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class ServerAdmin (admin.ModelAdmin):
    list_display = ['id','name','username','balance','customPassword', 'joinDate']

    def customPassword(self, obj):
        return '*' * 20
    customPassword.short_description = 'password'

admin.site.register(Server , ServerAdmin)