from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from .serializers import AnimalSerializer, CustomUserSerializer, NgoUserSerializer
from .models import Animal, CustomUser, NgoUser

class AnimalView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AnimalSerializer
    queryset = Animal.objects.all()

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong Email or password"}, status=status.HTTP_400_BAD_REQUEST)
        

class CustomUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = CustomUserSerializer(CustomUser.objects.get(user__email=request.user.email)).data
        res = serializer.pop('user') | serializer
        return Response(res, status=status.HTTP_200_OK)
    
    
class NgoUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = NgoUserSerializer(NgoUser.objects.get(user__email=request.user.email)).data
        res = serializer.pop('user') | serializer
        return Response(res, status=status.HTTP_200_OK)


class CustomUserRegistration(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token, _ = Token.objects.get_or_create(user=user.user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NgoUserRegistration(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = NgoUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token, _ = Token.objects.get_or_create(user=user.user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)