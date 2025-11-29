from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Vehicle
from .serializers import VehicleSerializer
from .permissions import RolePermission

class VehicleViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet provides create/retrieve/update/partial_update/destroy/list.
    RolePermission restricts which HTTP methods are allowed per role.
    """
    queryset = Vehicle.objects.all().order_by('-created_at')
    serializer_class = VehicleSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, RolePermission)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['vehicle_number', 'vehicle_model', 'vehicle_type']
    ordering_fields = ['created_at', 'vehicle_number']
