from django.contrib import admin
from .models import Animal, BaseUser, NgoUser, CustomUser, Campaign

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'user_email', 'user_phone', 
                  'animal_type', 'numberOfAnimals', 'description', 
                  'condition', 'image', 'latitude', 'longitude',
                  'address', 'landmark', 'status', 'reported_time',
                  'response_time', 'assigned_to')


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('ngo_name', 'title', 'description', 'tags', 'phone_number', 
                  'email', 'start_date', 'end_date', 'application_deadline', 
                  'age_group', 'image_link', 'is_over', 'campaign_id', 'applicant_list')


class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phone_number', 'is_ngo', 'is_active', 
                    'is_staff', 'is_superuser', 'date_joined', 'notify_token')
    search_fields = ['email', 'name', 'phone_number']

class NgoUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'emergency_contact_number', 'animals_supported',
                    'website', 'address', 'latitude', 'longitude', 'no_received_reports', 'created_campaigns_id')
    
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'no_reports', 'level', 'coins', 'applied_campaigns')
    


admin.site.register(Animal, AnimalAdmin)
admin.site.register(BaseUser, BaseUserAdmin)
admin.site.register(NgoUser, NgoUserAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Campaign, CampaignAdmin)