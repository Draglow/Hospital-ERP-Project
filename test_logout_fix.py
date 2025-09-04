#!/usr/bin/env python
"""
Quick test to verify logout functionality
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_erp.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

def test_logout_functionality():
    """Test logout functionality for both mobile and desktop"""
    print("🧪 Testing Logout Functionality...")
    print("=" * 50)
    
    # Create test user if doesn't exist
    try:
        user = User.objects.get(username='admin')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='admin',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print("Created test user: admin")
    
    # Test desktop logout
    print("\n1. Testing Desktop Logout...")
    desktop_client = Client(HTTP_USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
    
    # Login first
    login_response = desktop_client.login(username='admin', password='admin123')
    if login_response:
        print("✅ Desktop login successful")
        
        # Test logout
        logout_response = desktop_client.get(reverse('accounts:logout'))
        if logout_response.status_code == 302:
            print("✅ Desktop logout successful - redirected properly")
            print(f"   Redirect URL: {logout_response.url}")
        else:
            print(f"❌ Desktop logout failed - status: {logout_response.status_code}")
    else:
        print("❌ Desktop login failed")
    
    # Test mobile logout
    print("\n2. Testing Mobile Logout...")
    mobile_client = Client(HTTP_USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)')
    
    # Login first
    login_response = mobile_client.login(username='admin', password='admin123')
    if login_response:
        print("✅ Mobile login successful")
        
        # Test logout with mobile parameter
        logout_response = mobile_client.get(reverse('accounts:logout') + '?mobile=1')
        if logout_response.status_code == 302:
            print("✅ Mobile logout successful - redirected properly")
            print(f"   Redirect URL: {logout_response.url}")
        else:
            print(f"❌ Mobile logout failed - status: {logout_response.status_code}")
    else:
        print("❌ Mobile login failed")
    
    # Test URL resolution
    print("\n3. Testing URL Resolution...")
    try:
        logout_url = reverse('accounts:logout')
        print(f"✅ Logout URL resolves to: {logout_url}")
    except Exception as e:
        print(f"❌ URL resolution failed: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 Test Summary:")
    print("If you see ✅ for all tests above, logout functionality is working.")
    print("If you see ❌, there may be an issue with the logout implementation.")
    
    print("\n📋 Manual Testing Steps:")
    print("1. Start server: python manage.py runserver")
    print("2. Login at: http://localhost:8000/accounts/login/")
    print("3. Try logout from both desktop and mobile views")
    print("4. Verify you're redirected to login page")

if __name__ == '__main__':
    test_logout_functionality()
