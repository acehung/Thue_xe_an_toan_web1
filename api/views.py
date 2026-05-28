from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
import json
import logging

# Import logging utilities
from api.utils import log_user_action, log_failed_login, get_client_ip
from api.models import AuditLog, Vehicle
from api.serializers import VehicleSerializer

logger = logging.getLogger('api')

def index(request):
    return render(request, 'index.html')


@api_view(['GET'])
@permission_classes([AllowAny])
def vehicle_map(request):
    """
    View để hiển thị bản đồ vị trí các xe
    """
    return render(request, 'vehicle_map.html')

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    API để đăng ký
    Nhận: name, phone, email, password, cccd
    Trả về: success message hoặc error
    """
    try:
        # Parse request data - hỗ trợ JSON và form-data
        if request.content_type == 'application/json' or request.body:
            try:
                data = json.loads(request.body.decode('utf-8'))
            except (json.JSONDecodeError, ValueError):
                data = request.POST
        else:
            data = request.POST
        
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        cccd = data.get('cccd', '').strip()
        
        # Validation
        if not all([name, phone, email, password, cccd]):
            log_user_action(request, 'register', 'User', status_code=400)
            return Response(
                {'error': 'Vui lòng điền đầy đủ thông tin'},
                status=400
            )
        
        if len(password) < 8:
            log_user_action(request, 'register', 'User', status_code=400)
            return Response(
                {'error': 'Mật khẩu tối thiểu 8 ký tự'},
                status=400
            )
        
        # Kiểm tra email đã tồn tại
        if User.objects.filter(email=email).exists():
            log_failed_login(request, email, reason='Email already registered')
            return Response(
                {'error': 'Email đã được đăng ký'},
                status=400
            )
        
        # Kiểm tra username (dùng email làm username)
        if User.objects.filter(username=email).exists():
            log_failed_login(request, email, reason='Username already exists')
            return Response(
                {'error': 'Tài khoản này đã tồn tại'},
                status=400
            )
        
        # Tạo user mới
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )
        
        # Log successful registration
        log_user_action(
            request, 
            'register', 
            'User', 
            resource_id=user.id,
            new_values={'email': email, 'name': name},
            status_code=201
        )
        
        logger.info(f"New user registered: {email}")
        
        return Response({
            'success': True,
            'message': 'Đăng ký thành công',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'name': user.first_name,
            }
        }, status=201)
        
    except Exception as e:
        log_user_action(request, 'register', 'User', status_code=500)
        logger.error(f"Registration error: {str(e)}")
        return Response(
            {'error': f'Lỗi: {str(e)}'},
            status=500
        )

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    API để đăng nhập
    Nhận: username (email hoặc phone), password
    Trả về: access token, refresh token
    """
    try:
        # Parse request data - hỗ trợ JSON và form-data
        if request.content_type == 'application/json' or request.body:
            try:
                data = json.loads(request.body.decode('utf-8'))
            except (json.JSONDecodeError, ValueError):
                data = request.POST
        else:
            data = request.POST
        
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            log_failed_login(request, username or 'unknown', reason='Missing username or password')
            return Response(
                {'error': 'Vui lòng nhập email/phone và mật khẩu'},
                status=400
            )
        
        # Try authenticate with request parameter
        user = authenticate(request, username=username, password=password)
        
        # If that fails, try without request parameter
        if user is None:
            user = authenticate(username=username, password=password)
            
        if user is not None:
            # Log successful login
            log_user_action(
                request,
                'login',
                'User',
                resource_id=user.id,
                status_code=200
            )
            logger.info(f"User logged in: {username}")
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            # Log failed login attempt
            log_failed_login(request, username, reason='Invalid credentials')
            logger.warning(f"Failed login attempt for username: {username}")
            return Response(
                {'error': 'Sai thông tin đăng nhập'},
                status=401
            )
            
    except Exception as e:
        log_user_action(request, 'login', 'User', status_code=500)
        logger.error(f"Login exception: {str(e)}")
        return Response(
            {'error': f'Lỗi: {str(e)}'},
            status=500
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    API để đăng xuất
    Yêu cầu xác thực (phải đăng nhập trước)
    """
    try:
        # Log logout action
        log_user_action(
            request,
            'logout',
            'User',
            resource_id=request.user.id,
            status_code=200
        )
        logger.info(f"User logged out: {request.user.username}")
        
        return Response({
            'success': True,
            'message': 'Đăng xuất thành công'
        })
    except Exception as e:
        logger.error(f"Logout exception: {str(e)}")
        return Response(
            {'error': f'Lỗi: {str(e)}'},
            status=500
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_vehicles(request):
    """
    API để lấy danh sách tất cả xe với vị trí GPS hiện tại
    Trả về: Danh sách xe với tọa độ (lat, lng), trạng thái, tên, v.v.
    """
    try:
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response({
            'success': True,
            'count': len(vehicles),
            'vehicles': serializer.data
        }, status=200)
    except Exception as e:
        logger.error(f"Get vehicles exception: {str(e)}")
        return Response(
            {'error': f'Lỗi: {str(e)}'},
            status=500
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_vehicle_detail(request, vehicle_id):
    """
    API để lấy chi tiết xe theo ID
    """
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
        serializer = VehicleSerializer(vehicle)
        return Response({
            'success': True,
            'vehicle': serializer.data
        }, status=200)
    except Vehicle.DoesNotExist:
        return Response(
            {'error': 'Xe không tìm thấy'},
            status=404
        )
    except Exception as e:
        logger.error(f"Get vehicle detail exception: {str(e)}")
        return Response(
            {'error': f'Lỗi: {str(e)}'},
            status=500
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_vehicle_location(request, vehicle_id):
    """
    API để cập nhật vị trí GPS của xe
    Nhận: latitude, longitude, location_name (optional)
    """
    try:
        if request.content_type == 'application/json' or request.body:
            try:
                data = json.loads(request.body.decode('utf-8'))
            except (json.JSONDecodeError, ValueError):
                data = request.POST
        else:
            data = request.POST
        
        vehicle = Vehicle.objects.get(id=vehicle_id)
        
        # Cập nhật vị trí
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        location_name = data.get('location_name', '')
        
        if latitude is not None:
            vehicle.latitude = float(latitude)
        if longitude is not None:
            vehicle.longitude = float(longitude)
        if location_name:
            vehicle.location_name = location_name
        
        vehicle.save()
        
        # Log action
        log_user_action(
            request,
            'update',
            'Vehicle',
            resource_id=vehicle_id,
            new_values={
                'latitude': vehicle.latitude,
                'longitude': vehicle.longitude,
                'location_name': vehicle.location_name
            },
            status_code=200
        )
        
        serializer = VehicleSerializer(vehicle)
        return Response({
            'success': True,
            'message': 'Cập nhật vị trí thành công',
            'vehicle': serializer.data
        }, status=200)
    except Vehicle.DoesNotExist:
        return Response(
            {'error': 'Xe không tìm thấy'},
            status=404
        )
    except Exception as e:
        logger.error(f"Update vehicle location exception: {str(e)}")
        return Response(
            {'error': f'Lỗi: {str(e)}'},
            status=500
        )
