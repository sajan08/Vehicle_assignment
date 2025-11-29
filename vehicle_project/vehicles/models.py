from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    ROLE_SUPER = 'super'
    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'
    ROLE_CHOICES = [
        (ROLE_SUPER, 'Super admin'),
        (ROLE_ADMIN, 'Admin'),
        (ROLE_USER, 'User'),
    ]
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default=ROLE_USER)

    def is_super_admin(self):
        return self.role == self.ROLE_SUPER

    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def is_user(self):
        return self.role == self.ROLE_USER

class Vehicle(models.Model):
    VEHICLE_TWO = 'Two wheelers'
    VEHICLE_THREE = 'Three wheelers'
    VEHICLE_FOUR = 'Four wheelers'
    VEHICLE_TYPE_CHOICES = [
        (VEHICLE_TWO, 'Two wheelers'),
        (VEHICLE_THREE, 'Three wheelers'),
        (VEHICLE_FOUR, 'Four wheelers'),
    ]

    alnum_validator = RegexValidator(r'^[0-9A-Za-z-]+$',
                                     'Vehicle number must be alphanumeric (you may include "-").')

    vehicle_number = models.CharField(max_length=64, unique=True, validators=[alnum_validator])
    vehicle_type = models.CharField(max_length=32, choices=VEHICLE_TYPE_CHOICES)
    vehicle_model = models.CharField(max_length=128)
    vehicle_description = models.TextField(blank=True, default='')
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicles_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle_number} ({self.vehicle_type})"
