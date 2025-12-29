from django.db import models
from django.utils import timezone

# Create your models here.
class Server(models.Model):
    name = models.CharField(max_length=15)
    # number = models.CharField(unique=True, max_length=11)
    email = models.EmailField(max_length=30, unique=True)
    password = models.CharField(max_length=20)
    joinDate = models.DateTimeField(auto_now_add=True)

    def customDate(self):
        return timezone.localtime(self.joinDate).strftime('%d/%m/%y - %I:%M %p')

    def __str__(self):
        return self.name
    
