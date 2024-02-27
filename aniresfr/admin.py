from django.contrib import admin
from .models import Animal, BaseUser, NgoUser, CustomUser

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'user_phone', 
                  'animal_type','numberOfAnimals', 'description', 'condition',
                  'image', 'latitude', 'longitude','address', 'landmark',
                  'status', 'timestamp')
    
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phone_number', 'is_ngo', 'is_active', 
                    'is_staff', 'is_superuser', 'date_joined')

class NgoUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'emergency_contact_number', 'animals_supported',
                    'website', 'address', 'latitude', 'longitude')
    
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'coins')
    


admin.site.register(Animal, AnimalAdmin)
admin.site.register(BaseUser, BaseUserAdmin)
admin.site.register(NgoUser, NgoUserAdmin)
admin.site.register(CustomUser, CustomUserAdmin)