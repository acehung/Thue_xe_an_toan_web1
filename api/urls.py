from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.vehicle_map, name='vehicle_map'),
    
    # Auth endpoints
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # Vehicle endpoints
    path('vehicles/', views.get_vehicles, name='get_vehicles'),
    path('vehicles/<int:vehicle_id>/', views.get_vehicle_detail, name='get_vehicle_detail'),
    path('vehicles/<int:vehicle_id>/location/', views.update_vehicle_location, name='update_vehicle_location'),
]
