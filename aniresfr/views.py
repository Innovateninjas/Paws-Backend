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
from .notify import send_notification
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@csrf_exempt
def check_ngo(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        if not id:
            return JsonResponse({'error': 'ID not provided'}, status=400)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
            'Accept-Language': 'en,en-US;q=0.5',
            'Referer': 'https://ngodarpan.gov.in/index.php/search/',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        headers['Cookie'] = ''
        response = requests.get('https://ngodarpan.gov.in/index.php/ajaxcontroller/get_csrf', headers=headers)
        q = response.json()
        csrf = q["csrf_token"]

        headers['Accept'] = '*/*'
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        headers['Origin'] = 'https://ngodarpan.gov.in'
        headers['Cookie'] = 'ci_session=; ngd_csrf_cookie_name=' + csrf

        data = {
            'state_search': '',
            'district_search': '',
            'sector_search': 'null',
            'ngo_type_search': 'null',
            'ngo_name_search': '',
            'unique_id_search': id,
            'view_type': 'detail_view',
            'csrf_test_name': csrf,
        }

        response = requests.post('https://ngodarpan.gov.in/index.php/ajaxcontroller/search_index_new/0', headers=headers, data=data)

        # Check if an NGO is found
        ngo_exists = '<td><a href="javascript:void(0);"' in response.text

        return JsonResponse({'ngo_exists': ngo_exists})

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

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
            animal = Animal.objects.get(id=kwargs.get('pk')) 
            user = BaseUser.objects.get(email=animal.user_email)  
            if not user.notify_token:
                return response
            if request.data.get('status') == 'Rescued':
                send_notification([user.notify_token], 'Animal Rescued', 'Your Report has been resolved.')
            if request.data.get('status') == 'In Progress':
                send_notification([user.notify_token], 'Ngo on the Way', 'Your Report is being worked on.')
            if request.data.get('status') == 'Dead':
                send_notification([user.notify_token], '😔', 'Sorry, the animal could not be saved.')
            if request.data.get('status') == 'Not Found':
                send_notification([user.notify_token], 'Animal Not Found', 'Sorry, the animal was not found.')
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


class UploadProfilePhoto(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        profile_image = request.data.get("profile_image")
        

        try:
            user = BaseUser.objects.get(email=email)
        except BaseUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.profile_image = profile_image
        user.save()

        return Response({"message": "profile upload successfully"}, status=status.HTTP_200_OK)