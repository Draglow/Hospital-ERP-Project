#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_erp.settings')
django.setup()

from accounts.models import User

def create_superuser():
    """Create a superuser if it doesn't exist"""
    username = 'admin'
    email = 'admin@ethiopianhospital.com'
    password = 'admin123'
    
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='System',
            last_name='Administrator',
            role='admin'
        )
        print(f'Superuser created successfully!')
        print(f'Username: {username}')
        print(f'Password: {password}')
        print(f'Email: {email}')
    else:
        print('Superuser already exists!')

if __name__ == '__main__':
    create_superuser()
