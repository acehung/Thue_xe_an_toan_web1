import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.insert(0, 'e:\\autorent_backend')
django.setup()

from django.core.management import call_command

print("Creating migrations...")
call_command('makemigrations')

print("\nApplying migrations...")
call_command('migrate')

print("\nMigrations completed!")
