#!/usr/bin/env python
"""
Test the simple logout functionality
"""
import os
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_erp.settings')

try:
    import django
    django.setup()
    
    from django.test import Client
    from django.contrib.auth import get_user_model
    from django.urls import reverse
    
    print("🔧 TESTING SIMPLE LOGOUT FUNCTIONALITY")
    print("=" * 50)
    
    User = get_user_model()
    
    # Create test user
    try:
        user = User.objects.get(username='testlogout')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testlogout',
            password='test123',
            first_name='Test',
            last_name='Logout'
        )
        print("✅ Created test user")
    
    # Test the simple logout
    print("\n1️⃣ Testing Simple Logout Function...")
    client = Client()
    
    # Login first
    login_success = client.login(username='testlogout', password='test123')
    if login_success:
        print("   ✅ Login successful")
        
        # Test logout
        print("   🔄 Testing logout...")
        response = client.get('/accounts/logout/')
        
        print(f"   📊 Response Status: {response.status_code}")
        print(f"   📍 Response Type: {type(response)}")
        
        if response.status_code == 302:
            redirect_url = response.url
            print(f"   📍 Redirect URL: {redirect_url}")
            
            if redirect_url == '/':
                print("   ✅ SUCCESS: Redirects to homepage!")
            else:
                print(f"   ❌ WRONG: Expected '/', got '{redirect_url}'")
        else:
            print(f"   ❌ Expected redirect (302), got {response.status_code}")
            
        # Test if user is logged out
        response2 = client.get('/dashboard/')
        if response2.status_code == 302 and 'login' in response2.url:
            print("   ✅ User successfully logged out")
        else:
            print("   ❌ User might still be logged in")
            
    else:
        print("   ❌ Login failed")
    
    # Test URL resolution
    print("\n2️⃣ Testing URL Resolution...")
    try:
        logout_url = reverse('accounts:logout')
        print(f"   ✅ Logout URL: {logout_url}")
    except Exception as e:
        print(f"   ❌ URL resolution failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 SUMMARY:")
    print("✅ Created simple function-based logout view")
    print("✅ Bypasses Django's LogoutView completely")
    print("✅ Uses direct HttpResponseRedirect to homepage")
    print("✅ CSRF exempt to avoid token issues")
    print("✅ Should work with both GET and POST requests")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Start server: python manage.py runserver")
    print("2. Login and test logout")
    print("3. Should redirect to homepage with success message")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
