from django.db import models
from .manager import UserManager
import uuid
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin


GENDER_CHOICES = (('male','Male'),('female','Female'))
MERITAL_STATUS = (('single','Single'),('married','Married'))

class User(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    name = models.CharField(max_length=255,blank=True)
    email = models.EmailField(unique=True,max_length=100,verbose_name="email",blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True,unique=True)
    gender = models.CharField(max_length=20,choices=GENDER_CHOICES,blank=True,null=True)
    merital_status = models.CharField(max_length=20,choices=MERITAL_STATUS,blank=True,null=True)
    birthday = models.DateField(verbose_name='birthday', blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    pin = models.CharField(max_length=6,blank=True,null=True)
    state = models.CharField(max_length=50,blank=True,null=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    provider = models.CharField(max_length=100,choices=(('email','Email'),('google','Google'),('phone','Phone')),blank=True)
    otp = models.CharField(max_length=10,null=True,blank=True)
    pwd_reset_token = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email or self.phone
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
            return self.is_admin

    def has_module_perms(self, app_label):
            return self.is_admin