from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, 'index.html')

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
        data = json.loads(request.body) if isinstance(request.body, bytes) else request.POST
        
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        cccd = data.get('cccd', '').strip()
        
        # Validation
        if not all([name, phone, email, password, cccd]):
            return Response(
                {'error': 'Vui lòng điền đầy đủ thông tin'},
                status=400
            )
        
        if len(password) < 8:
            return Response(
                {'error': 'Mật khẩu tối thiểu 8 ký tự'},
                status=400
            )
        
        # Kiểm tra email đã tồn tại
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Email đã được đăng ký'},
                status=400
            )
        
        # Kiểm tra username (dùng email làm username)
        if User.objects.filter(username=email).exists():
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
        data = json.loads(request.body) if isinstance(request.body, bytes) else request.POST
        username = data.get('username')
        password = data.get('password')
        
        print(f"[LOGIN] Username: {username}, Password: {password}")
        
        if not username or not password:
            print("[LOGIN] Missing username or password")
            return Response(
                {'error': 'Vui lòng nhập email/phone và mật khẩu'},
                status=400
            )
        
        # Try authenticate with request parameter
        user = authenticate(request, username=username, password=password)
        print(f"[LOGIN] Authenticate result (with request): {user}")
        
        # If that fails, try without request parameter
        if user is None:
            user = authenticate(username=username, password=password)
            print(f"[LOGIN] Authenticate result (without request): {user}")
            
        if user is not None:
            print(f"[LOGIN] User authenticated: {user}")
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            print(f"[LOGIN] Authentication failed for username: {username}")
            return Response(
                {'error': 'Sai thông tin đăng nhập'},
                status=401
            )
            
    except Exception as e:
        print(f"[LOGIN] Exception: {str(e)}")
        return Response(
            {'error': f'Lỗi: {str(e)}'},
            status=500
        )
