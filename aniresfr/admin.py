from django.contrib import admin
from .models import Animal, NgoUser, CustomUser

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'user_phone', 
                  'animal_type','numberOfAnimals', 'description', 'condition',
                  'image', 'latitude', 'longitude','address', 'landmark',
                  'status', 'timestamp')
    
class NgoUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'emergency_contact_number',
                    'website', 'address', 'latitude', 'longitude')
    
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'level', 'coins')

admin.site.register(Animal, AnimalAdmin)
admin.site.register(NgoUser, NgoUserAdmin)
admin.site.register(CustomUser, CustomUserAdmin)