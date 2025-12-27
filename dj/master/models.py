from django.db import models

# Create your models here.
class Server(models.Model):
    name = models.CharField(max_length=15)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
