from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


def one_day_from_now():
    return timezone.now() + timedelta(days=1)


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
    reported_time = models.DateTimeField(auto_now_add=True)
    response_time = models.DateTimeField(default=one_day_from_now)
    assigned_to = models.CharField(max_length=200, default='None')

    def __str__(self):
        return self.description


class Campaign(models.Model):
    ngo_name = models.CharField(max_length=200)
    title = models.TextField()
    description = models.TextField()
    tags = models.JSONField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    application_deadline = models.DateTimeField()
    age_group = models.IntegerField()
    image_link = models.URLField(blank=True, null=True)
    is_over = models.BooleanField(default=False)
    campaign_id = models.AutoField(primary_key=True)
    applicant_list = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title


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


class NgoUser(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)
    emergency_contact_number = models.CharField(max_length=15, default='')
    animals_supported = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    website = models.CharField(max_length=200, default='')
    address = models.CharField(max_length=500, default='')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    no_received_reports = models.IntegerField(default=0)
    created_campaigns_id = ArrayField(models.IntegerField(), blank=True, default=list)

    def __str__(self):
        return self.user.name


class CustomUser(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)
    no_reports = models.IntegerField(default=0)
    applied_campaigns = ArrayField(models.IntegerField(), blank=True, default=list)
    level = models.IntegerField(default=1)
    coins = models.IntegerField(default=0)

    def __str__(self):
        return self.user.name