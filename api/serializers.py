from rest_framework import serializers
from api.models import Vehicle, AuditLog


class VehicleSerializer(serializers.ModelSerializer):
    """Serializer cho Vehicle model"""
    class Meta:
        model = Vehicle
        fields = [
            'id', 'name', 'license_plate', 'vehicle_type', 
            'latitude', 'longitude', 'location_name', 'status',
            'color', 'year', 'price_per_day',
            'created_at', 'updated_at', 'last_location_update'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_location_update']


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer cho AuditLog model"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'user_username', 'action', 'resource', 'resource_id',
            'ip_address', 'user_agent', 'http_method', 'endpoint',
            'status_code', 'error_message', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']
