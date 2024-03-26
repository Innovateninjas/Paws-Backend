from .models import *
from django.db.models import F
from rest_framework import serializers
from django.contrib.auth import get_user_model
from math import radians, cos, sin, sqrt, atan2
from .notify import send_notification


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 'user_name', 'user_email', 'user_phone', 
                  'animal_type', 'numberOfAnimals', 'description', 
                  'condition', 'image', 'latitude', 'longitude',
                  'address', 'landmark', 'status', 'reported_time',
                  'response_time', 'assigned_to']
        
    def create(self, validated_data):
        animal = Animal.objects.create(**validated_data)
        ngos = NgoUser.objects.all()
        min_distance = None
        nearest_ngo = None
        for ngo in ngos:
            dlon = radians(ngo.longitude) - radians(animal.longitude)
            dlat = radians(ngo.latitude) - radians(animal.latitude)
            a = sin(dlat / 2)**2 + cos(radians(animal.latitude)) * cos(radians(ngo.latitude)) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = 6371.01 * c
            if min_distance is None or distance < min_distance:
                min_distance = distance
                nearest_ngo = ngo
                print(nearest_ngo.user.email, distance)
        if nearest_ngo is not None:
            animal.assigned_to = nearest_ngo.user.email
            nearest_ngo.no_received_reports = F('no_received_reports') + 1
            nearest_ngo.save(update_fields=['no_received_reports'])
            animal.save()
            send_notification([nearest_ngo.user.notify_token], 'New Report', 'A new report has been made near you.')
        return animal


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['ngo_name', 'title', 'description', 'tags', 'phone_number', 
                  'email', 'start_date', 'end_date', 'application_deadline', 
                  'age_group', 'image_link', 'is_over', 'campaign_id', 'applicant_list']
        
    def create(self, validated_data):
        campaign = Campaign.objects.create(**validated_data)
        users = CustomUser.objects.all()
        registration_tokens = [user.user.notify_token for user in users if user.user.notify_token]
        send_notification(registration_tokens, 'New Campaign', 'participate in :'+campaign.title+' campaign.')
        return campaign

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'phone_number', 'is_ngo', 'date_joined', 'notify_token']


class CustomUserSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)
    email = serializers.EmailField(write_only=True)
    name = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['user', 'email', 'name', 'phone_number',
                   'password', 'level', 'coins', 'no_reports',
                   'applied_campaigns']

    def create(self, validated_data):
        BaseUser = get_user_model()
        base_user = BaseUser.objects.create_user(
            email=validated_data.pop('email'),
            name=validated_data.pop('name'),
            phone_number=validated_data.pop('phone_number'),
            password=validated_data.pop('password'),
        )
        custom_user = CustomUser.objects.create(user=base_user, **validated_data)
        return custom_user


class NgoUserSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)
    email = serializers.EmailField(write_only=True)
    name = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = NgoUser
        fields = ['user', 'email', 'name', 'phone_number', 
                  'password', 'emergency_contact_number', 
                  'animals_supported', 'website', 'address', 
                  'latitude', 'longitude', 'no_received_reports',
                  'created_campaigns_id']

    def create(self, validated_data):
        BaseUser = get_user_model()
        base_user = BaseUser.objects.create_user(
            email=validated_data.pop('email'),
            name=validated_data.pop('name'),
            phone_number=validated_data.pop('phone_number'),
            password=validated_data.pop('password'),
            is_ngo=True,
        )
        ngo_user = NgoUser.objects.create(user=base_user, **validated_data)
        return ngo_user