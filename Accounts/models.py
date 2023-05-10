from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
from rest_framework.authtoken.models import Token


#we just need to make a manager class using BaseUserManager and overide the create_user and create_superuser
class UserManager(BaseUserManager):
    x = 1/0
    print(x)
    def create_superuser(self,username,email,password,**other_fields):
        other_fields.setdefault('is_active',True)
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned is_staff as True'))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be assigned is_superuser as True'))
        return self.create_user(email=email,username=username,password=password,**other_fields)
    
    def create_user(self,email,username,password,**other_fields):
        if not email:
            raise ValueError(_('User must have a email'))
        if not username:
            raise ValueError(_('User must have a username'))
        
        email = self.normalize_email(email)
        user = self.model(email=email,username=username,**other_fields)
        user.set_password(password)
        user.save()
        return user
        
        
            
#here we create new user by extending to two classes, AbstractBaseUser used to make users and PermissionMixin to authorize the user using default sercurity method given in django

class NewUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(verbose_name="email",max_length=60,unique=True)
    username = models.CharField(max_length=40,unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add = True)
    last_login = models.DateTimeField(verbose_name='last login',auto_now=True)
    
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
    
    def __str__(self):
        return self.username
    
#this creates a token everytime a new user is created in the token database that has one to one relationship with the user table
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance = None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)