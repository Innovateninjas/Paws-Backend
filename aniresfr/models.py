from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext as _


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


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class NgoUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    emergency_contact_number = models.CharField(max_length=15)
    animals_supported = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    website = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number', 'emergency_contact_number']

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='ngo_user_groups'  # Change this to a unique related name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='ngo_user_permissions'  # Change this to a unique related name
    )

    def __str__(self):
        return self.name
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    level = models.IntegerField(default=1)
    coins = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_groups'  # Change this to a unique related name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_permissions'  # Change this to a unique related name
    )

    def __str__(self):
        return self.email