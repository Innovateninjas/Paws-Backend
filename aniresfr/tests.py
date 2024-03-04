from django.test import TestCase, Client
from django.urls import reverse
from .models import Animal, BaseUser, NgoUser

class AnimalViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = BaseUser.objects.create_user(email='testuser', password='testpass', name = 'testuser', phone_number = '1234567890')
        self.ngo_user = NgoUser.objects.create(user=self.user, latitude=22.0, longitude=89.0)
        self.user2 = BaseUser.objects.create_user(email='testuser2', password='testpass2',  name = 'testuser2', phone_number = '1234567890')
        self.ngo_user2 = NgoUser.objects.create(user=self.user2, latitude=22.0, longitude=87.5)
        self.animal_data = {
            'user_name': 'testuser',
            'user_email': 'testuser@example.com',
            'user_phone': '1234567890',
            'animal_type': 'Dog',
            'numberOfAnimals': 1,
            'description': 'Test description',
            'condition': 'Healthy',
            'latitude': 22.0,
            'longitude': 88.0,
            'address': 'Test address',
            'landmark': 'Test landmark',
            'status': 'Reported',
            'image': 'Testimage.wq',
            'reported_time': '2022-01-01T00:00:00Z'}

    def test_create_animal(self):
        response = self.client.post(reverse('animal-list'), self.animal_data, format='json')
        print(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)