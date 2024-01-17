from django.shortcuts import render
from rest_framework import viewsets
from .serializers import AnimalSerializer
from .models import Animal

class AnimalView(viewsets.ModelViewSet):
    serializer_class = AnimalSerializer
    queryset = Animal.objects.all()
