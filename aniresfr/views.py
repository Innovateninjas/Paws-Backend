from django.db import IntegrityError
from regex import P
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets, filters
from .serializers import AnimalSerializer, CustomUserSerializer, NgoUserSerializer, CampaignSerializer
from .models import Animal, CustomUser, NgoUser, Campaign


def get_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token.key


class AnimalView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AnimalSerializer
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `user_email` query parameter in the URL.
        """
        queryset =Animal.objects.all()
        user_email = self.request.query_params.get('user_email')
        if user_email is not None:
            queryset = queryset.filter(user_email=user_email)
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