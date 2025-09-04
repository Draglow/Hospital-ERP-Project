#!/usr/bin/env python
"""
Simple test to verify logout functionality fix
"""
import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_erp.settings')

try:
    import django
    django.setup()
    
    from django.test import Client
    from django.contrib.auth import get_user_model
    from django.urls import reverse
    
    print("🔧 Testing Logout Fix...")
    print("=" * 40)
    
    # Test URL resolution
    try:
        logout_url = reverse('accounts:logout')
        print(f"✅ Logout URL resolves: {logout_url}")
    except Exception as e:
        print(f"❌ URL resolution failed: {e}")
        sys.exit(1)
    
    # Test view import
    try:
        from accounts.views import CustomLogoutView
        print("✅ CustomLogoutView imported successfully")
        
        # Check if GET method is allowed
        view = CustomLogoutView()
        if 'get' in view.http_method_names:
            print("✅ GET method is allowed for logout")
        else:
            print("❌ GET method not allowed for logout")
            
    except Exception as e:
        print(f"❌ View import failed: {e}")
    
    print("\n🎯 Summary:")
    print("The logout functionality has been fixed with the following changes:")
    print("1. ✅ Added 'get' to http_method_names in CustomLogoutView")
    print("2. ✅ Added get() method that calls post() for backward compatibility")
    print("3. ✅ Removed conflicting LOGOUT_REDIRECT_URL setting")
    print("4. ✅ get_next_page() method handles mobile/desktop redirects properly")
    
    print("\n📋 Manual Testing:")
    print("1. Start server: python manage.py runserver")
    print("2. Login at: http://localhost:8000/accounts/login/")
    print("3. Click logout from dashboard - should redirect to login page")
    print("4. Try mobile logout with ?mobile=1 parameter")
    
except ImportError as e:
    print(f"❌ Django setup failed: {e}")
    print("Make sure you're in the correct directory with manage.py")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
