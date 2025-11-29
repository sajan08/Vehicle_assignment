from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import CustomUser, Vehicle
from rest_framework.authtoken.models import Token

class BaseAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # users
        self.super_user = CustomUser.objects.create_user(username='super', password='pass', role=CustomUser.ROLE_SUPER)
        self.admin_user = CustomUser.objects.create_user(username='admin', password='pass', role=CustomUser.ROLE_ADMIN)
        self.normal_user = CustomUser.objects.create_user(username='user', password='pass', role=CustomUser.ROLE_USER)

        # tokens
        for u in (self.super_user, self.admin_user, self.normal_user):
            Token.objects.create(user=u)

        # create a vehicle by super
        self.vehicle = Vehicle.objects.create(vehicle_number='MH-02-BT-9884', vehicle_type='Two', vehicle_model='Honda', vehicle_description='Nice')

class RolePermissionTest(BaseAPITest):
    def test_super_can_create_and_delete(self):
        token = Token.objects.get(user=self.super_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        resp = self.client.post('/api/vehicles/', {
            'vehicle_number': 'MH-02-BT-9884', 'vehicle_type': 'Four wheelers', 'vehicle_model': 'Tesla', 'vehicle_description': 'Electric'
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        vid = resp.data['id']

        # delete
        resp2 = self.client.delete(f'/api/vehicles/{vid}/')
        self.assertIn(resp2.status_code, (204, 200))

    def test_admin_cannot_create_or_delete_but_can_edit(self):
        token = Token.objects.get(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        # create attempt
        resp = self.client.post('/api/vehicles/', {
            'vehicle_number': 'MH-02-BT-9884', 'vehicle_type': 'Two Wheeler', 'vehicle_model': 'Yamaha', 'vehicle_description': 'Bike'
        }, format='json')
        self.assertEqual(resp.status_code, 403)

        # admin can edit existing vehicle
        resp2 = self.client.patch(f'/api/vehicles/{self.vehicle.id}/', {'vehicle_model': 'UpdatedModel'}, format='json')
        self.assertIn(resp2.status_code, (200, 202))

        # delete attempt
        resp3 = self.client.delete(f'/api/vehicles/{self.vehicle.id}/')
        self.assertEqual(resp3.status_code, 403)

    def test_user_can_only_view(self):
        token = Token.objects.get(user=self.normal_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        resp = self.client.get('/api/vehicles/')
        self.assertEqual(resp.status_code, 200)

        resp2 = self.client.patch(f'/api/vehicles/{self.vehicle.id}/', {'vehicle_model': 'X'}, format='json')
        self.assertEqual(resp2.status_code, 403)

        resp3 = self.client.post('/api/vehicles/', {
            'vehicle_number': 'MH-02-BT-9884', 'vehicle_type': 'Two Wheeler', 'vehicle_model': 'Hero', 'vehicle_description': 'Bad'
        }, format='json')
        self.assertEqual(resp3.status_code, 403)
