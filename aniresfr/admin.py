from django.contrib import admin
from .models import Animal

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'user_phone', 
                  'animal_type', 'description', 'condition',
                  'image', 'latitude', 'longitude', 'landmark',
                  'status')

admin.site.register(Animal, AnimalAdmin)