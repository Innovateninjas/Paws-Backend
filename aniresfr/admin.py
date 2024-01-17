from django.contrib import admin
from .models import Animal

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'animal_type', 'condition', 'phone_number', 'latitude', 'longitude', 'landmark')

admin.site.register(Animal, AnimalAdmin)