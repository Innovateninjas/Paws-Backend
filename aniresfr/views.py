from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from .serializers import *
from .models import *
from notify import send_notification


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
    
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        if request.data.get('status') != 'Received':
            user = BaseUser.objects.get(email=request.data.get('user_email'))
            if request.data.get('status') == 'Rescued':
                send_notification([user.notify_token], 'Animal Rescued', 'Your Report has been resolved.')
            if request.data.get('status') == 'In Progress':
                send_notification([user.notify_token], 'Ngo on the Way', 'Your Report is being worked on.')
        return response


class CampaignView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.all()

class NearestNgoView(APIView):
    permission_classes = [AllowAny]

    def get_data(self, serializer):
        info = serializer.data
        data = info.pop('user') | info
        return data
    
    def get(self, request):
        lat = float(request.query_params.get('lat'))
        lon = float(request.query_params.get('lon'))

        ngos = NgoUser.objects.all()
        min_distance = None
        nearest_ngo = None
        for ngo in ngos:
            dlon = radians(ngo.longitude) - radians(lon)
            dlat = radians(ngo.latitude) - radians(lat)
            a = sin(dlat / 2)**2 + cos(radians(lat)) * cos(radians(ngo.latitude)) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = 6371.01 * c
            if min_distance is None or distance < min_distance:
                min_distance = distance
                nearest_ngo = ngo

        if nearest_ngo is not None:
            return Response(self.get_data(NgoUserSerializer(nearest_ngo)))
        else:
            return Response({
                'error': 'No NGOs found',
            })
        

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


class UpdateNotifyTokenView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        token = request.data.get("token")
        user = request.user
        user.notify_token = token
        user.save()
        return Response({"message": "Token updated successfully"}, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        phone_number = request.data.get("phone_number")
        new_password = request.data.get("new_password")

        try:
            user = BaseUser.objects.get(email=email, phone_number=phone_number)
        except BaseUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.password = make_password(new_password)
        user.save()

        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

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