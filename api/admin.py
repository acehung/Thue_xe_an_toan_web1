from django.contrib import admin
from django.utils.html import format_html
from .models import AuditLog, Vehicle


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    Admin interface for AuditLog model
    Cho phép xem lịch sử hoạt động của người dùng
    """
    list_display = ('timestamp', 'user_display', 'action_colored', 'resource', 'ip_address', 'status_code')
    list_filter = ('action', 'resource', 'timestamp', 'status_code')
    search_fields = ('user__username', 'ip_address', 'resource', 'error_message')
    readonly_fields = ('user', 'action', 'resource', 'resource_id', 'ip_address', 'user_agent', 
                       'http_method', 'endpoint', 'status_code', 'error_message', 'old_values', 
                       'new_values', 'timestamp')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'ip_address', 'user_agent')
        }),
        ('Request Information', {
            'fields': ('http_method', 'endpoint', 'status_code')
        }),
        ('Action Information', {
            'fields': ('action', 'resource', 'resource_id')
        }),
        ('Data Changes', {
            'fields': ('old_values', 'new_values'),
            'classes': ('collapse',)
        }),
        ('Error Information', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        }),
    )
    
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'
    
    def user_display(self, obj):
        """Display user with link to admin"""
        if obj.user:
            return format_html(
                '<a href="/admin/auth/user/{}/change/">{}</a>',
                obj.user.id,
                obj.user.username
            )
        return 'Anonymous'
    user_display.short_description = 'User'
    
    def action_colored(self, obj):
        """Display action with color based on type"""
        colors = {
            'login': '#28a745',  # Green
            'logout': '#6c757d',  # Gray
            'register': '#17a2b8',  # Blue
            'create': '#007bff',  # Blue
            'update': '#ffc107',  # Yellow
            'delete': '#dc3545',  # Red
            'failed_login': '#dc3545',  # Red
            'permission_denied': '#fd7e14',  # Orange
        }
        color = colors.get(obj.action, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_action_display()
        )
    action_colored.short_description = 'Action'
    
    def has_add_permission(self, request):
        """Không cho phép tạo audit log qua admin"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Chỉ superuser mới có thể xóa audit log"""
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        """Không cho phép chỉnh sửa audit log"""
        return False


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """
    Admin interface for Vehicle model
    Quản lý thông tin xe và vị trí GPS
    """
    list_display = ('name', 'license_plate', 'vehicle_type', 'status_colored', 'location_name', 'price_per_day', 'last_location_update')
    list_filter = ('status', 'vehicle_type', 'year', 'created_at')
    search_fields = ('name', 'license_plate', 'location_name')
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'license_plate', 'vehicle_type', 'color', 'year')
        }),
        ('Vị trí GPS', {
            'fields': ('latitude', 'longitude', 'location_name', 'last_location_update')
        }),
        ('Trạng thái & Giá', {
            'fields': ('status', 'price_per_day')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_location_update')
    ordering = ('-created_at',)
    
    def status_colored(self, obj):
        """Display status with color"""
        colors = {
            'available': '#28a745',      # Green
            'rented': '#ff9800',         # Orange
            'maintenance': '#dc3545',    # Red
            'inactive': '#6c757d',       # Gray
        }
        color = colors.get(obj.status, '#6c757d')
        status_text = {
            'available': 'Có sẵn',
            'rented': 'Đang cho thuê',
            'maintenance': 'Bảo trì',
            'inactive': 'Không hoạt động'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            status_text.get(obj.status, obj.status)
        )
    status_colored.short_description = 'Trạng thái'
