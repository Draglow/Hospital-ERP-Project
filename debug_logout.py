#!/usr/bin/env python
"""
Debug script to test logout URLs and see what's happening
"""
import os
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_erp.settings')

try:
    import django
    django.setup()
    
    from django.urls import reverse, resolve
    from django.test import Client
    from django.contrib.auth import get_user_model
    
    print("🔍 DEBUGGING LOGOUT ISSUE")
    print("=" * 40)
    
    # Test URL resolution
    print("\n1️⃣ URL Resolution Test:")
    try:
        accounts_logout = reverse('accounts:logout')
        homepage = reverse('homepage')
        print(f"✅ accounts:logout resolves to: {accounts_logout}")
        print(f"✅ homepage resolves to: {homepage}")
        
        # Test what view handles the logout URL
        resolver = resolve('/accounts/logout/')
        print(f"✅ /accounts/logout/ handled by: {resolver.func.__name__}")
        print(f"✅ View class: {resolver.func.view_class}")
        
    except Exception as e:
        print(f"❌ URL resolution failed: {e}")
    
    # Test actual logout behavior
    print("\n2️⃣ Logout Behavior Test:")
    User = get_user_model()
    
    # Create test user
    try:
        user = User.objects.get(username='debuguser')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='debuguser',
            password='debug123',
            first_name='Debug',
            last_name='User'
        )
        print("✅ Created debug user")
    
    # Test logout
    client = Client()
    login_success = client.login(username='debuguser', password='debug123')
    
    if login_success:
        print("✅ Login successful")
        
        # Test logout
        print("🔄 Testing logout...")
        response = client.get('/accounts/logout/')
        
        print(f"📊 Status Code: {response.status_code}")
        if response.status_code == 302:
            print(f"📍 Redirect Location: {response.url}")
            print(f"📍 Redirect Headers: {response.get('Location', 'None')}")
        
        # Check if it's our custom view
        if hasattr(response, 'context') and response.context:
            print(f"📄 Context: {response.context}")
        
    else:
        print("❌ Login failed")
    
    print("\n3️⃣ Possible Issues:")
    print("- Are you clicking the right logout link?")
    print("- Check if you're in Django admin (/admin/) when logging out")
    print("- Verify the logout link URL in browser developer tools")
    print("- Check browser network tab to see actual request URL")
    
    print("\n4️⃣ Correct Logout URLs:")
    print(f"✅ Desktop: {accounts_logout}")
    print(f"✅ Mobile: {accounts_logout}?mobile=1")
    print("❌ Wrong: /admin/logout/ (Django admin logout)")
    
except Exception as e:
    print(f"❌ Debug failed: {e}")
    import traceback
    traceback.print_exc()
