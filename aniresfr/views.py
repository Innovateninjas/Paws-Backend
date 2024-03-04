from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from .serializers import *
from .models import *


def get_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token.key


class AnimalView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AnimalSerializer
    def get_queryset(self):
        queryset =Animal.objects.all()
        user_email = self.request.query_params.get('user_email', None)
        assigned_to = self.request.query_params.get('assigned_to', None)

        if user_email is not None:
            queryset = queryset.filter(user_email=user_email)
        if assigned_to is not None:
            queryset = queryset.filter(assigned_to=assigned_to)
        return queryset


class CampaignView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.all()


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            data={'token': get_token(user), 'is_ngo': user.is_ngo}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong Email or password"}, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
    

class CustomUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return CustomUser.objects.get(user__email=self.request.user.email)
    
    def get_data(self, serializer):
        info = serializer.data
        data = info.pop('user') | info
        return data

    def get(self, request):
        serializer = CustomUserSerializer(self.get_object())
        return Response(self.get_data(serializer), status=status.HTTP_200_OK)
    
    def put(self, request):
        serializer = CustomUserSerializer(self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(self.get_data(serializer), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class NgoUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return NgoUser.objects.select_related('user').get(user__email=self.request.user.email)
    
    def get_data(self, serializer):
        info = serializer.data
        data = info.pop('user') | info
        return data
    
    def get(self, request):
        serializer = NgoUserSerializer(self.get_object())
        return Response(self.get_data(serializer), status=status.HTTP_200_OK)
    
    def put(self, request):
        serializer = NgoUserSerializer(self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(self.get_data(serializer), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NgoView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, email):
        return NgoUser.objects.select_related('user').get(user__email=email)

    def get_data(self, serializer):
        info = serializer.data
        data = info.pop('user') | info
        return data

    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            list = []
            for ngo_user in NgoUser.objects.select_related('user').all():
                serializer = NgoUserSerializer(ngo_user)
                list.append(self.get_data(serializer))
            return Response(list, status=status.HTTP_200_OK)
        ngo_user = self.get_object(email)
        serializer = NgoUserSerializer(ngo_user)
        return Response(self.get_data(serializer), status=status.HTTP_200_OK)


class CustomUserRegistration(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = serializer.save()
            return Response({'token': get_token(user.user)}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            raise ValidationError({'error': 'The account with that Email already exists. Please Login.'})


class NgoUserRegistration(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = NgoUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = serializer.save()
            return Response({'token': get_token(user.user)}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            raise ValidationError({'error': 'The account with that Email already exists. Please Login.'})