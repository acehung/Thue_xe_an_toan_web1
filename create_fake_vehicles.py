import os
import sys
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.insert(0, 'e:\\autorent_backend')
django.setup()

from api.models import Vehicle
from decimal import Decimal

# Fake vehicle data with locations in Ho Chi Minh City and Hanoi
FAKE_VEHICLES = [
    # Ho Chi Minh City vehicles
    {
        'name': 'Toyota Vios 2023',
        'license_plate': 'SG-001-AA',
        'vehicle_type': 'Sedan',
        'latitude': 10.7769,
        'longitude': 106.6966,
        'location_name': 'District 1, HCMC',
        'status': 'available',
        'color': 'White',
        'year': 2023,
        'price_per_day': Decimal('500000'),
    },
    {
        'name': 'Honda City 2022',
        'license_plate': 'SG-002-AA',
        'vehicle_type': 'Sedan',
        'latitude': 10.8017,
        'longitude': 106.7171,
        'location_name': 'District 3, HCMC',
        'status': 'rented',
        'color': 'Silver',
        'year': 2022,
        'price_per_day': Decimal('450000'),
    },
    {
        'name': 'Hyundai i10 2023',
        'license_plate': 'SG-003-AA',
        'vehicle_type': 'Hatchback',
        'latitude': 10.7538,
        'longitude': 106.6262,
        'location_name': 'District 7, HCMC',
        'status': 'available',
        'color': 'Red',
        'year': 2023,
        'price_per_day': Decimal('350000'),
    },
    {
        'name': 'Toyota Fortuner 2022',
        'license_plate': 'SG-004-AA',
        'vehicle_type': 'SUV',
        'latitude': 10.8447,
        'longitude': 106.7604,
        'location_name': 'Thu Duc, HCMC',
        'status': 'available',
        'color': 'Black',
        'year': 2022,
        'price_per_day': Decimal('900000'),
    },
    {
        'name': 'Kia Cerato 2021',
        'license_plate': 'SG-005-AA',
        'vehicle_type': 'Sedan',
        'latitude': 10.9268,
        'longitude': 106.8408,
        'location_name': 'Binh Thanh, HCMC',
        'status': 'maintenance',
        'color': 'Blue',
        'year': 2021,
        'price_per_day': Decimal('550000'),
    },
    {
        'name': 'Mitsubishi Xpander 2023',
        'license_plate': 'SG-006-AA',
        'vehicle_type': 'MPV',
        'latitude': 10.7292,
        'longitude': 106.6747,
        'location_name': 'District 5, HCMC',
        'status': 'available',
        'color': 'Red',
        'year': 2023,
        'price_per_day': Decimal('700000'),
    },
    # Hanoi vehicles
    {
        'name': 'Toyota Camry 2022',
        'license_plate': 'HN-001-AA',
        'vehicle_type': 'Sedan',
        'latitude': 21.0285,
        'longitude': 105.8542,
        'location_name': 'Hoan Kiem, Hanoi',
        'status': 'available',
        'color': 'White',
        'year': 2022,
        'price_per_day': Decimal('800000'),
    },
    {
        'name': 'Ford Ranger 2023',
        'license_plate': 'HN-002-AA',
        'vehicle_type': 'Pickup',
        'latitude': 21.0549,
        'longitude': 105.8581,
        'location_name': 'Cau Giay, Hanoi',
        'status': 'rented',
        'color': 'Gray',
        'year': 2023,
        'price_per_day': Decimal('750000'),
    },
    {
        'name': 'Honda Civic 2021',
        'license_plate': 'HN-003-AA',
        'vehicle_type': 'Sedan',
        'latitude': 20.9927,
        'longitude': 105.7893,
        'location_name': 'Ba Dinh, Hanoi',
        'status': 'available',
        'color': 'Black',
        'year': 2021,
        'price_per_day': Decimal('650000'),
    },
    {
        'name': 'Mazda CX-5 2023',
        'license_plate': 'HN-004-AA',
        'vehicle_type': 'SUV',
        'latitude': 21.0069,
        'longitude': 105.8471,
        'location_name': 'Dong Da, Hanoi',
        'status': 'available',
        'color': 'Silver',
        'year': 2023,
        'price_per_day': Decimal('900000'),
    },
]

def populate_vehicles():
    """Create fake vehicle data"""
    print("Populating vehicles...")
    
    # Clear existing vehicles if needed
    # Vehicle.objects.all().delete()
    
    created_count = 0
    for vehicle_data in FAKE_VEHICLES:
        # Check if vehicle already exists by license plate
        if not Vehicle.objects.filter(license_plate=vehicle_data['license_plate']).exists():
            vehicle = Vehicle.objects.create(**vehicle_data)
            print(f"✓ Created: {vehicle.name} ({vehicle.license_plate})")
            created_count += 1
        else:
            print(f"⚠ Already exists: {vehicle_data['license_plate']}")
    
    print(f"\nTotal vehicles created: {created_count}")
    print(f"Total vehicles in database: {Vehicle.objects.count()}")

if __name__ == '__main__':
    populate_vehicles()
