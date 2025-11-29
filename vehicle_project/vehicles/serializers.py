from rest_framework import serializers
from .models import Vehicle
import bleach

ALLOWED_TAGS = [] 
ALLOWED_ATTRS = {}

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'id', 'vehicle_number', 'vehicle_type', 'vehicle_model',
            'vehicle_description', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ('created_by', 'created_at', 'updated_at',)

    def validate_vehicle_number(self, value):
        # Already validated by model validator but adding extra sanity
        v = value.strip()
        if not v:
            raise serializers.ValidationError("Vehicle number cannot be empty.")
        return bleach.clean(v, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)

    def validate_vehicle_model(self, value):
        return bleach.clean(value.strip(), tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)

    def validate_vehicle_description(self, value):
        # strip and sanitize free text to prevent XSS
        return bleach.clean(value.strip(), tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)
