from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from .serializers import AnimalSerializer, CustomUserSerializer, NgoUserSerializer, CampaignSerializer
from .models import Animal, CustomUser, NgoUser, Campaign


def get_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token.key


class AnimalView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AnimalSerializer
    queryset = Animal.objects.all()


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
        

class CustomUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        custom_user = CustomUser.objects.select_related('user').get(user__email=request.user.email)
        serializer = CustomUserSerializer(custom_user).data
        data = serializer.pop('user') | serializer
        return Response(data, status=status.HTTP_200_OK)
    
    
class NgoUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        ngo_user = NgoUser.objects.select_related('user').get(user__email=request.user.email)
        serializer = NgoUserSerializer(ngo_user).data
        data = serializer.pop('user') | serializer
        return Response(data, status=status.HTTP_200_OK)


class CustomUserRegistration(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({'token': get_token(user.user)}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            raise ValidationError({'error': 'The account with that Email already exists. Please Login.'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NgoUserRegistration(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = NgoUserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({'token': get_token(user.user)}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            raise ValidationError({'error': 'The account with that Email already exists. Please Login.'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)