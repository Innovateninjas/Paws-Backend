from rest_framework import serializers
from .models import Animal, NgoUser, CustomUser


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'


class NgoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NgoUser
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'