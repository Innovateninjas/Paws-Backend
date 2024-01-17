from django.db import models

class Animal(models.Model):
    name = models.CharField(max_length=200)
    animal_type = models.CharField(max_length=200)
    condition = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    latitude = models.FloatField()
    longitude = models.FloatField()
    landmark = models.CharField(max_length=200)

    def __str__(self):
        return self.name