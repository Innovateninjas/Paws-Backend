from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Animal, NgoUser, CustomUser, Campaign


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 'user_name', 'user_email', 'user_phone', 
                  'animal_type', 'numberOfAnimals', 'description', 
                  'condition', 'image', 'latitude', 'longitude',
                  'address', 'landmark', 'status', 'reported_time',
                  'response_time', 'assigned_to']


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['ngo_name', 'title', 'description', 'tags', 'phone_number', 
                  'email', 'start_date', 'end_date', 'application_deadline', 
                  'age_group', 'image_link', 'is_over', 'campaign_id', 'applicant_list']


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'phone_number', 'is_ngo', 'date_joined']


class CustomUserSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)
    email = serializers.EmailField(write_only=True)
    name = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['user', 'email', 'name', 'phone_number',
                   'password', 'level', 'coins', 'no_reports']

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
                  'latitude', 'longitude', 'no_received_reports']

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