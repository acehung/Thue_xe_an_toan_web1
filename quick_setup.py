import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.insert(0, 'e:\\autorent_backend')
django.setup()

from django.core.management import call_command

print("=" * 60)
print("  Creating Migrations...")
print("=" * 60)
call_command('makemigrations')

print("\n" + "=" * 60)
print("  Applying Migrations...")
print("=" * 60)
call_command('migrate')

print("\n✅ Migrations complete!")
print("\nNow creating sample vehicles...")

from api.models import Vehicle
from decimal import Decimal

vehicles_data = [
    ('Toyota Vios 2023', 'SG-001-AA', 'Sedan', 10.7769, 106.6966, 'District 1, HCMC', 'available', 'White', 2023, 500000),
    ('Honda City 2022', 'SG-002-AA', 'Sedan', 10.8017, 106.7171, 'District 3, HCMC', 'rented', 'Silver', 2022, 450000),
    ('Hyundai i10 2023', 'SG-003-AA', 'Hatchback', 10.7538, 106.6262, 'District 7, HCMC', 'available', 'Red', 2023, 350000),
    ('Toyota Fortuner 2022', 'SG-004-AA', 'SUV', 10.8447, 106.7604, 'Thu Duc, HCMC', 'available', 'Black', 2022, 900000),
    ('Kia Cerato 2021', 'SG-005-AA', 'Sedan', 10.9268, 106.8408, 'Binh Thanh, HCMC', 'maintenance', 'Blue', 2021, 550000),
    ('Mitsubishi Xpander 2023', 'SG-006-AA', 'MPV', 10.7292, 106.6747, 'District 5, HCMC', 'available', 'Red', 2023, 700000),
    ('Toyota Camry 2022', 'HN-001-AA', 'Sedan', 21.0285, 105.8542, 'Hoan Kiem, Hanoi', 'available', 'White', 2022, 800000),
    ('Ford Ranger 2023', 'HN-002-AA', 'Pickup', 21.0549, 105.8581, 'Cau Giay, Hanoi', 'rented', 'Gray', 2023, 750000),
    ('Honda Civic 2021', 'HN-003-AA', 'Sedan', 20.9927, 105.7893, 'Ba Dinh, Hanoi', 'available', 'Black', 2021, 650000),
    ('Mazda CX-5 2023', 'HN-004-AA', 'SUV', 21.0069, 105.8471, 'Dong Da, Hanoi', 'available', 'Silver', 2023, 900000),
]

created = 0
for name, plate, vtype, lat, lng, location, status, color, year, price in vehicles_data:
    if not Vehicle.objects.filter(license_plate=plate).exists():
        Vehicle.objects.create(
            name=name,
            license_plate=plate,
            vehicle_type=vtype,
            latitude=lat,
            longitude=lng,
            location_name=location,
            status=status,
            color=color,
            year=year,
            price_per_day=Decimal(price)
        )
        print(f"✓ {name} ({plate})")
        created += 1

print(f"\n✅ Created {created} vehicles")
print(f"📊 Total vehicles: {Vehicle.objects.count()}")
