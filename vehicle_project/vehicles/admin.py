from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Vehicle

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_number', 'vehicle_type', 'vehicle_model', 'created_by', 'created_at')
    search_fields = ('vehicle_number', 'vehicle_model')
