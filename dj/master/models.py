from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from decimal import Decimal
from django.conf import settings

class MyUserManager(BaseUserManager):
    def create_user(self, name, username, password=None):
        if not username:
            raise ValueError('without UserName')
        user = self.model(username=username , name=name,)
        user.set_password(password)

        user.save(using=self._db)
        return user
    
    def create_superuser(self, name, username, password=None):
        user = self.create_user(
            name=name,
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
class Server(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=20)
    username = models.CharField(max_length=30, unique=True)
    joinDate = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
        
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.username
    

class Transaction(models.Model):
    # transactionType = (('s', 'Suceessfull'), ('f', 'Faile'))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name= 'transactions'
    )
    name = models.CharField(max_length=100)
    amount = models.CharField(max_length=1000)
    charge = models.CharField(max_length=1000, default='No Charge')
    status = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.name} - {self.amount}'