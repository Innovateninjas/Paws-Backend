from django.db import models


class Animal(models.Model):
    user_name = models.CharField(max_length=200)
    user_email = models.EmailField()
    user_phone = models.CharField(max_length=15)
    animal_type = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    condition = models.CharField(max_length=50)
    image = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    landmark = models.CharField(max_length=200)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.description