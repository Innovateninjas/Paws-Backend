from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class BaseUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    is_ngo= models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Animal(models.Model):
    user_name = models.CharField(max_length=200)
    user_email = models.EmailField()
    user_phone = models.CharField(max_length=15)
    animal_type = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    condition = models.CharField(max_length=50)
    image = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    numberOfAnimals = models.CharField(max_length=15)
    address = models.CharField(max_length=500)
    landmark = models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class NgoUser(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)
    emergency_contact_number = models.CharField(max_length=15, default='')
    animals_supported = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    website = models.CharField(max_length=200, default='')
    address = models.CharField(max_length=500, default='')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.name
    

class CustomUser(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)
    level = models.IntegerField(default=1)
    coins = models.IntegerField(default=0)

    def __str__(self):
        return self.user.name