# api/utils/logging_utils.py
"""
Utility functions cho logging và audit trail
"""

import logging
from django.http import HttpRequest
from api.models import AuditLog

# Get loggers
logger = logging.getLogger('api')
audit_logger = logging.getLogger('audit')
security_logger = logging.getLogger('security')


def get_client_ip(request: HttpRequest) -> str:
    """
    Lấy IP thực của client (tính đến proxy)
    Kiểm tra X-Forwarded-For header nếu có
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    return ip


def log_user_action(request: HttpRequest, action: str, resource: str, resource_id=None,
                    old_values=None, new_values=None, status_code=200):
    """
    Ghi lại hành động của người dùng vào database (AuditLog) và file log
    
    Args:
        request: Django request object
        action: Loại hành động (login, logout, create, update, delete, etc)
        resource: Loại resource (User, Booking, Car, etc)
        resource_id: ID của resource được thao tác
        old_values: Dict giá trị cũ (cho update operations)
        new_values: Dict giá trị mới (cho update operations)
        status_code: HTTP status code
    """
    try:
        user = request.user if request.user.is_authenticated else None
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        http_method = request.method
        endpoint = request.path
        
        # Ghi vào database
        AuditLog.log_action(
            user=user,
            action=action,
            resource=resource,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            http_method=http_method,
            endpoint=endpoint,
            status_code=status_code,
            old_values=old_values,
            new_values=new_values,
        )
        
        # Ghi vào file log
        user_str = user.username if user else 'Anonymous'
        message = f"{action.upper()} - {resource}:{resource_id} - User:{user_str} - IP:{ip_address} - Status:{status_code}"
        audit_logger.info(message)
        
    except Exception as e:
        logger.error(f"Error logging audit action: {str(e)}")


def log_failed_login(request: HttpRequest, username: str, reason: str = 'Invalid credentials'):
    """
    Ghi lại lần đăng nhập thất bại
    Cảnh báo về các cuộc tấn công brute force
    """
    try:
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        
        AuditLog.log_action(
            user=None,
            action='failed_login',
            resource='User',
            ip_address=ip_address,
            user_agent=user_agent,
            http_method='POST',
            endpoint='/api/login/',
            status_code=401,
            error_message=f"Failed login attempt - {reason} - Username: {username}",
        )
        
        # Cảnh báo bảo mật nếu có nhiều lần thất bại
        failed_count = AuditLog.objects.filter(
            action='failed_login',
            ip_address=ip_address
        ).count()
        
        if failed_count >= 5:
            security_logger.warning(
                f"Multiple failed login attempts from IP {ip_address} - "
                f"Total attempts: {failed_count} - Username: {username}"
            )
        
    except Exception as e:
        logger.error(f"Error logging failed login: {str(e)}")


def log_permission_denied(request: HttpRequest, resource: str, reason: str = 'Permission denied'):
    """
    Ghi lại các truy cập bị từ chối do thiếu quyền
    Giúp phát hiện các cuộc tấn công
    """
    try:
        user = request.user if request.user.is_authenticated else None
        ip_address = get_client_ip(request)
        
        AuditLog.log_action(
            user=user,
            action='permission_denied',
            resource=resource,
            ip_address=ip_address,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            http_method=request.method,
            endpoint=request.path,
            status_code=403,
            error_message=reason,
        )
        
        security_logger.warning(
            f"Permission denied - User:{user.username if user else 'Anonymous'} - "
            f"Resource:{resource} - IP:{ip_address}"
        )
        
    except Exception as e:
        logger.error(f"Error logging permission denied: {str(e)}")


def log_api_error(request: HttpRequest, error_message: str, error_code: int = 500):
    """
    Ghi lại lỗi API
    """
    try:
        user = request.user if request.user.is_authenticated else None
        
        AuditLog.log_action(
            user=user,
            action='error',
            resource='API',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            http_method=request.method,
            endpoint=request.path,
            status_code=error_code,
            error_message=error_message,
        )
        
    except Exception as e:
        logger.error(f"Error logging API error: {str(e)}")


def log_sensitive_operation(request: HttpRequest, operation: str, details: str):
    """
    Ghi lại các hoạt động nhạy cảm (rút tiền, xóa tài khoản, etc)
    """
    try:
        user = request.user if request.user.is_authenticated else None
        
        AuditLog.log_action(
            user=user,
            action='sensitive_operation',
            resource='Sensitive',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            http_method=request.method,
            endpoint=request.path,
            error_message=f"{operation} - {details}",
        )
        
        security_logger.info(
            f"SENSITIVE OP - {operation} - User:{user.username if user else 'Anonymous'} - {details}"
        )
        
    except Exception as e:
        logger.error(f"Error logging sensitive operation: {str(e)}")
