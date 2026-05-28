#!/usr/bin/env python
"""
AutoRent Vehicle Tracking System - Setup Script

This script sets up the vehicle tracking system:
1. Creates and applies migrations
2. Populates fake vehicle data
3. Verifies the setup

Run this after deploying the vehicle tracking feature.
"""

import os
import sys
import django
import subprocess

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.insert(0, 'e:\\autorent_backend')
django.setup()

from django.core.management import call_command
from api.models import Vehicle
from decimal import Decimal

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def run_migrations():
    """Create and apply migrations"""
    print_section("STEP 1: Running Migrations")
    
    try:
        print("\n📝 Creating migrations...")
        call_command('makemigrations', verbosity=1)
        
        print("\n✓ Applying migrations...")
        call_command('migrate', verbosity=1)
        
        print("\n✅ Migrations completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Migration error: {e}")
        return False

def populate_vehicles():
    """Populate fake vehicle data"""
    print_section("STEP 2: Populating Vehicle Data")
    
    vehicles_data = [
        # Ho Chi Minh City
        ('Toyota Vios 2023', 'SG-001-AA', 'Sedan', 10.7769, 106.6966, 'District 1, HCMC', 'available', 'White', 2023, 500000),
        ('Honda City 2022', 'SG-002-AA', 'Sedan', 10.8017, 106.7171, 'District 3, HCMC', 'rented', 'Silver', 2022, 450000),
        ('Hyundai i10 2023', 'SG-003-AA', 'Hatchback', 10.7538, 106.6262, 'District 7, HCMC', 'available', 'Red', 2023, 350000),
        ('Toyota Fortuner 2022', 'SG-004-AA', 'SUV', 10.8447, 106.7604, 'Thu Duc, HCMC', 'available', 'Black', 2022, 900000),
        ('Kia Cerato 2021', 'SG-005-AA', 'Sedan', 10.9268, 106.8408, 'Binh Thanh, HCMC', 'maintenance', 'Blue', 2021, 550000),
        ('Mitsubishi Xpander 2023', 'SG-006-AA', 'MPV', 10.7292, 106.6747, 'District 5, HCMC', 'available', 'Red', 2023, 700000),
        # Hanoi
        ('Toyota Camry 2022', 'HN-001-AA', 'Sedan', 21.0285, 105.8542, 'Hoan Kiem, Hanoi', 'available', 'White', 2022, 800000),
        ('Ford Ranger 2023', 'HN-002-AA', 'Pickup', 21.0549, 105.8581, 'Cau Giay, Hanoi', 'rented', 'Gray', 2023, 750000),
        ('Honda Civic 2021', 'HN-003-AA', 'Sedan', 20.9927, 105.7893, 'Ba Dinh, Hanoi', 'available', 'Black', 2021, 650000),
        ('Mazda CX-5 2023', 'HN-004-AA', 'SUV', 21.0069, 105.8471, 'Dong Da, Hanoi', 'available', 'Silver', 2023, 900000),
    ]
    
    created_count = 0
    skipped_count = 0
    
    print(f"\n📦 Creating {len(vehicles_data)} vehicles...\n")
    
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
            print(f"  ✓ {name} ({plate})")
            created_count += 1
        else:
            print(f"  ⚠ {plate} already exists")
            skipped_count += 1
    
    print(f"\n✅ Vehicles population completed!")
    print(f"   Created: {created_count}")
    print(f"   Skipped: {skipped_count}")
    return True

def verify_setup():
    """Verify the setup"""
    print_section("STEP 3: Verifying Setup")
    
    try:
        count = Vehicle.objects.count()
        statuses = Vehicle.objects.values('status').distinct()
        
        print(f"\n📊 Database Statistics:")
        print(f"   Total vehicles: {count}")
        print(f"\n   Status distribution:")
        for status_obj in statuses:
            status = status_obj['status']
            count = Vehicle.objects.filter(status=status).count()
            print(f"   - {status}: {count}")
        
        print(f"\n✅ Setup verification completed!")
        print(f"\n🎉 Vehicle tracking system is ready!")
        return True
    except Exception as e:
        print(f"\n❌ Verification error: {e}")
        return False

def main():
    """Run all setup steps"""
    print_section("AutoRent Vehicle Tracking System - Setup")
    print("\nThis script will set up the vehicle tracking feature with:")
    print("  • Database migrations")
    print("  • Sample vehicle data (10 vehicles)")
    print("  • Admin interface configuration")
    print("\nAccess the vehicle map at: http://127.0.0.1:8000/api/")
    
    # Run setup steps
    if not run_migrations():
        print("\n❌ Setup failed at migration step")
        return False
    
    if not populate_vehicles():
        print("\n❌ Setup failed at population step")
        return False
    
    if not verify_setup():
        print("\n⚠️ Setup completed but verification had issues")
        return False
    
    print_section("Setup Complete!")
    print("\n✅ Vehicle tracking system is ready to use!\n")
    print("📍 Access points:")
    print("   • Vehicle Map: http://127.0.0.1:8000/api/")
    print("   • API Vehicles: http://127.0.0.1:8000/api/vehicles/")
    print("   • Admin Panel: http://127.0.0.1:8000/admin/")
    print("\n🔧 You can now:")
    print("   • View all vehicles on the interactive map")
    print("   • Update vehicle locations via API")
    print("   • Manage vehicles in the admin panel")
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    main()
