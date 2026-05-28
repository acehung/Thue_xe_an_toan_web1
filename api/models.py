from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Vehicle(models.Model):
    """
    Model để lưu thông tin xe thuê và vị trí hiện tại
    """
    STATUS_CHOICES = [
        ('available', 'Còn trống'),
        ('rented', 'Đang cho thuê'),
        ('maintenance', 'Bảo trì'),
        ('inactive', 'Không hoạt động'),
    ]
    
    name = models.CharField(max_length=100, help_text='Tên xe (VD: Toyota Vios 2023)')
    license_plate = models.CharField(max_length=20, unique=True, help_text='Biển số xe')
    vehicle_type = models.CharField(max_length=50, help_text='Loại xe (Sedan, SUV, Van, etc)')
    
    # Tọa độ GPS hiện tại
    latitude = models.FloatField(default=10.7769, help_text='Vĩ độ')
    longitude = models.FloatField(default=106.6966, help_text='Kinh độ')
    location_name = models.CharField(max_length=255, blank=True, help_text='Tên địa điểm')
    
    # Trạng thái
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    # Thông tin khác
    color = models.CharField(max_length=50, blank=True)
    year = models.IntegerField(null=True, blank=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_location_update = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'
    
    def __str__(self):
        return f"{self.name} ({self.license_plate})"


class AuditLog(models.Model):
    """
    Model để lưu trữ tất cả hoạt động của người dùng
    Giúp theo dõi ai đã làm gì, khi nào, từ đâu
    """
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('register', 'Register'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('download', 'Download'),
        ('permission_denied', 'Permission Denied'),
        ('failed_login', 'Failed Login'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    resource = models.CharField(max_length=100, help_text='Model name (User, Booking, Car, etc)')
    resource_id = models.IntegerField(null=True, blank=True)
    
    # Store old and new values for update operations
    old_values = models.JSONField(null=True, blank=True)
    new_values = models.JSONField(null=True, blank=True)
    
    # Request info
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=500, blank=True)
    http_method = models.CharField(max_length=10, blank=True)  # GET, POST, PUT, DELETE, etc
    endpoint = models.CharField(max_length=255, blank=True)
    
    # Status info
    status_code = models.IntegerField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['resource', 'timestamp']),
            models.Index(fields=['ip_address', 'timestamp']),
        ]
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
    
    def __str__(self):
        user_str = self.user.username if self.user else 'Anonymous'
        return f"{self.action} - {self.resource} - {user_str} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    
    @classmethod
    def log_action(cls, user, action, resource, resource_id=None, ip_address='0.0.0.0',
                   user_agent='', http_method='', endpoint='', status_code=None, 
                   error_message='', old_values=None, new_values=None):
        """
        Tiện ích để ghi audit log
        
        Ví dụ:
        AuditLog.log_action(
            user=request.user,
            action='login',
            resource='User',
            resource_id=request.user.id,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
        )
        """
        return cls.objects.create(
            user=user,
            action=action,
            resource=resource,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            http_method=http_method,
            endpoint=endpoint,
            status_code=status_code,
            error_message=error_message,
            old_values=old_values,
            new_values=new_values,
        )
