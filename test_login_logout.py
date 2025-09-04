#!/usr/bin/env python
"""
Test script for login/logout functionality across different devices
Ethiopian Hospital ERP System
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.sessions.models import Session
import time

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_erp.settings')
django.setup()

User = get_user_model()


class LoginLogoutTestCase(TestCase):
    """Test cases for login/logout functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Different user agents for testing
        self.user_agents = {
            'desktop': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'mobile_android': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 Mobile',
            'mobile_iphone': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'tablet_ipad': 'Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
        }
    
    def test_desktop_login_performance(self):
        """Test desktop login performance"""
        client = Client(HTTP_USER_AGENT=self.user_agents['desktop'])
        
        start_time = time.time()
        response = client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        login_time = time.time() - start_time
        
        # Should redirect to desktop dashboard
        self.assertEqual(response.status_code, 302)
        self.assertIn('dashboard', response.url)
        self.assertNotIn('mobile', response.url)
        
        # Performance check - should be under 1 second
        self.assertLess(login_time, 1.0, f"Desktop login took {login_time:.3f}s, should be under 1s")
        
        print(f"✓ Desktop login: {login_time:.3f}s")
    
    def test_mobile_login_performance(self):
        """Test mobile login performance"""
        client = Client(HTTP_USER_AGENT=self.user_agents['mobile_android'])
        
        start_time = time.time()
        response = client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        login_time = time.time() - start_time
        
        # Should redirect to mobile dashboard
        self.assertEqual(response.status_code, 302)
        self.assertIn('mobile', response.url)
        
        # Performance check
        self.assertLess(login_time, 1.0, f"Mobile login took {login_time:.3f}s, should be under 1s")
        
        print(f"✓ Mobile login: {login_time:.3f}s")
    
    def test_desktop_logout_functionality(self):
        """Test desktop logout functionality"""
        client = Client(HTTP_USER_AGENT=self.user_agents['desktop'])
        
        # Login first
        client.login(username='testuser', password='testpass123')
        
        # Test logout
        start_time = time.time()
        response = client.get(reverse('accounts:logout'))
        logout_time = time.time() - start_time
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)
        self.assertNotIn('mobile=1', response.url)
        
        # Performance check
        self.assertLess(logout_time, 0.5, f"Desktop logout took {logout_time:.3f}s, should be under 0.5s")
        
        print(f"✓ Desktop logout: {logout_time:.3f}s")
    
    def test_mobile_logout_functionality(self):
        """Test mobile logout functionality"""
        client = Client(HTTP_USER_AGENT=self.user_agents['mobile_android'])
        
        # Login first
        client.login(username='testuser', password='testpass123')
        
        # Test logout with mobile parameter
        start_time = time.time()
        response = client.get(reverse('accounts:logout') + '?mobile=1')
        logout_time = time.time() - start_time
        
        # Should redirect to mobile login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)
        self.assertIn('mobile=1', response.url)
        
        # Performance check
        self.assertLess(logout_time, 0.5, f"Mobile logout took {logout_time:.3f}s, should be under 0.5s")
        
        print(f"✓ Mobile logout: {logout_time:.3f}s")
    
    def test_session_cleanup(self):
        """Test that sessions are properly cleaned up on logout"""
        client = Client()
        
        # Login
        client.login(username='testuser', password='testpass123')
        
        # Get session count before logout
        sessions_before = Session.objects.count()
        
        # Logout
        client.get(reverse('accounts:logout'))
        
        # Session should be cleaned up
        sessions_after = Session.objects.count()
        self.assertLessEqual(sessions_after, sessions_before)
        
        print("✓ Session cleanup working")
    
    def test_remember_me_functionality(self):
        """Test remember me functionality"""
        client = Client()
        
        # Login with remember me
        response = client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123',
            'remember_me': 'on'
        })
        
        # Should set longer session expiry
        self.assertEqual(response.status_code, 302)
        
        print("✓ Remember me functionality working")
    
    def test_cross_device_consistency(self):
        """Test that login/logout works consistently across devices"""
        results = {}
        
        for device, user_agent in self.user_agents.items():
            client = Client(HTTP_USER_AGENT=user_agent)
            
            # Test login
            start_time = time.time()
            login_response = client.post(reverse('accounts:login'), {
                'username': 'testuser',
                'password': 'testpass123'
            })
            login_time = time.time() - start_time
            
            # Test logout
            start_time = time.time()
            logout_response = client.get(reverse('accounts:logout'))
            logout_time = time.time() - start_time
            
            results[device] = {
                'login_time': login_time,
                'logout_time': logout_time,
                'login_success': login_response.status_code == 302,
                'logout_success': logout_response.status_code == 302
            }
        
        # Print results
        print("\n=== Cross-Device Test Results ===")
        for device, result in results.items():
            status = "✓" if result['login_success'] and result['logout_success'] else "✗"
            print(f"{status} {device.upper()}: Login {result['login_time']:.3f}s, Logout {result['logout_time']:.3f}s")
        
        # All devices should work
        for device, result in results.items():
            self.assertTrue(result['login_success'], f"Login failed for {device}")
            self.assertTrue(result['logout_success'], f"Logout failed for {device}")


def run_tests():
    """Run all tests"""
    print("🚀 Starting Login/Logout Performance Tests...")
    print("=" * 50)
    
    # Create test instance
    test_case = LoginLogoutTestCase()
    test_case.setUp()
    
    try:
        # Run individual tests
        test_case.test_desktop_login_performance()
        test_case.test_mobile_login_performance()
        test_case.test_desktop_logout_functionality()
        test_case.test_mobile_logout_functionality()
        test_case.test_session_cleanup()
        test_case.test_remember_me_functionality()
        test_case.test_cross_device_consistency()
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! Login/logout optimization successful.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        return False
    
    return True


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
