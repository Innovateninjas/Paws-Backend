# backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from aniresfr.models import CustomUser, NgoUser


class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(Q(email=username) | Q(phone_number=username))
            if user.password == password:
                return user
        except CustomUser.DoesNotExist:
            return None

class NgoUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = NgoUser.objects.get(Q(email=username) | Q(phone_number=username))
            if user.password == password:
                return user
        except NgoUser.DoesNotExist:
            return None

class TokenCustomUserBackend(ModelBackend):
    def authenticate(self, request, token=None, **kwargs):
        try:
            user = CustomUser.objects.get(token=token)
            return user
        except CustomUser.DoesNotExist:
            return None

