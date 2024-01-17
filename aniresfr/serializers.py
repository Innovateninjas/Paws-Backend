from rest_framework import serializers
from .models import Animal

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ('id', 'name', 'animal_type', 'condition', 'phone_number', 'latitude', 'longitude', 'landmark')