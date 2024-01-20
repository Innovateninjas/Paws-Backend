from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Animal

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ('id', 'user_name', 'user_email', 'user_phone', 
                  'animal_type', 'description', 'condition',
                  'image', 'latitude', 'longitude', 'landmark',
                  'status')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')