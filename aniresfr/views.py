from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from .serializers import AnimalSerializer, UserSerializer
from .models import Animal

class AnimalView(viewsets.ModelViewSet):
    serializer_class = AnimalSerializer
    queryset = Animal.objects.all()

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
class RegisterView(APIView):
    def post(self, request):
        fullName = request.data.get('fullName')
        phoneNumber = request.data.get('phoneNumber')
        email = request.data.get('email')
        password = request.data.get('password')
        user_type = request.data.get('userType')


        if not fullName or not phoneNumber or not email or not password:
            return Response({'error': 'fullName, phoneNumber, email, and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email is already in use'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=email, email=email, password=password, first_name=fullName, last_name=phoneNumber)

        # Get or create the group
        group, created = Group.objects.get_or_create(name=user_type)

        # Add the user to the group
        group.user_set.add(user)

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)