#!/usr/bin/env python3
"""
Simple Healthcare Dashboard Testing
Basic functionality tests without complex Django setup
"""

import os
import sys
import requests
import json
from datetime import datetime
import time

class SimpleHealthcareTest:
    """Simple test suite for healthcare dashboard"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = {
            'connectivity': {},
            'pages': {},
            'forms': {},
            'mobile': {},
            'performance': {}
        }
    
    def test_server_connectivity(self):
        """Test if the Django server is running"""
        print("Testing server connectivity...")
        
        try:
            response = self.session.get(self.base_url, timeout=10)
            self.test_results['connectivity'] = {
                'server_running': response.status_code in [200, 302, 404],
                'response_time': response.elapsed.total_seconds(),
                'status_code': response.status_code
            }
            print(f"✅ Server is running (Status: {response.status_code})")
            return True
        except requests.exceptions.RequestException as e:
            self.test_results['connectivity'] = {
                'server_running': False,
                'error': str(e)
            }
            print(f"❌ Server connection failed: {e}")
            return False
    
    def test_page_accessibility(self):
        """Test if main pages are accessible"""
        print("\nTesting page accessibility...")
        
        pages_to_test = [
            ('homepage', '/'),
            ('login', '/accounts/login/'),
            ('dashboard', '/dashboard/'),
            ('patients', '/dashboard/'),
            ('appointments', '/appointments/'),
            ('doctors', '/doctors/'),
            ('pharmacy', '/pharmacy/'),
            ('billing', '/billing/')
        ]
        
        for page_name, url in pages_to_test:
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}{url}", timeout=10)
                load_time = time.time() - start_time
                
                self.test_results['pages'][page_name] = {
                    'accessible': response.status_code in [200, 302],
                    'status_code': response.status_code,
                    'load_time': load_time,
                    'content_length': len(response.content),
                    'has_html': 'html' in response.text.lower()
                }
                
                if response.status_code in [200, 302]:
                    print(f"✅ {page_name}: Accessible ({response.status_code}) - {load_time:.2f}s")
                else:
                    print(f"❌ {page_name}: Not accessible ({response.status_code})")
                    
            except requests.exceptions.RequestException as e:
                self.test_results['pages'][page_name] = {
                    'accessible': False,
                    'error': str(e)
                }
                print(f"❌ {page_name}: Connection error - {e}")
    
    def test_static_files(self):
        """Test if static files are being served"""
        print("\nTesting static files...")
        
        static_files = [
            ('css', '/static/css/dashboard.css'),
            ('js', '/static/js/dashboard.js'),
            ('bootstrap_css', '/static/css/bootstrap.min.css'),
            ('fontawesome', '/static/css/all.min.css')
        ]
        
        for file_name, url in static_files:
            try:
                response = self.session.get(f"{self.base_url}{url}", timeout=5)
                
                self.test_results['pages'][f'static_{file_name}'] = {
                    'accessible': response.status_code == 200,
                    'status_code': response.status_code,
                    'content_length': len(response.content)
                }
                
                if response.status_code == 200:
                    print(f"✅ Static {file_name}: Available")
                else:
                    print(f"⚠️  Static {file_name}: Not found ({response.status_code})")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Static {file_name}: Error - {e}")
    
    def test_mobile_responsiveness(self):
        """Test mobile responsiveness by checking viewport meta tags"""
        print("\nTesting mobile responsiveness...")
        
        try:
            # Test homepage for mobile optimization
            response = self.session.get(self.base_url, timeout=10)
            content = response.text.lower()
            
            mobile_tests = {
                'viewport_meta': 'viewport' in content and 'width=device-width' in content,
                'responsive_css': 'col-' in content or 'row' in content or '@media' in content,
                'bootstrap': 'bootstrap' in content,
                'mobile_friendly_nav': 'navbar-toggler' in content or 'hamburger' in content,
                'touch_friendly': 'btn-lg' in content or 'touch' in content
            }
            
            self.test_results['mobile'] = mobile_tests
            
            for test_name, result in mobile_tests.items():
                if result:
                    print(f"✅ Mobile {test_name}: Present")
                else:
                    print(f"⚠️  Mobile {test_name}: Not detected")
                    
        except requests.exceptions.RequestException as e:
            self.test_results['mobile'] = {'error': str(e)}
            print(f"❌ Mobile testing failed: {e}")
    
    def test_ui_elements(self):
        """Test for UI elements and styling"""
        print("\nTesting UI elements...")
        
        try:
            response = self.session.get(self.base_url, timeout=10)
            content = response.text.lower()
            
            ui_tests = {
                'glassmorphism': 'backdrop-filter' in content or 'glass' in content,
                'animations': 'animation' in content or 'transition' in content,
                'ethiopian_colors': 'ethiopia' in content or '#009639' in content or '#0f47af' in content,
                'fontawesome_icons': 'fas fa-' in content or 'fab fa-' in content,
                'cards': 'card' in content,
                'buttons': 'btn' in content,
                'forms': 'form' in content,
                'navigation': 'nav' in content
            }
            
            self.test_results['pages']['ui_elements'] = ui_tests
            
            for test_name, result in ui_tests.items():
                if result:
                    print(f"✅ UI {test_name}: Present")
                else:
                    print(f"⚠️  UI {test_name}: Not detected")
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ UI testing failed: {e}")
    
    def test_form_accessibility(self):
        """Test if forms are accessible"""
        print("\nTesting form accessibility...")
        
        try:
            # Test login form
            response = self.session.get(f"{self.base_url}/accounts/login/", timeout=10)
            content = response.text.lower()
            
            form_tests = {
                'login_form': 'username' in content and 'password' in content,
                'csrf_protection': 'csrfmiddlewaretoken' in content,
                'form_validation': 'required' in content,
                'labels': 'label' in content,
                'submit_button': 'submit' in content or 'login' in content
            }
            
            self.test_results['forms'] = form_tests
            
            for test_name, result in form_tests.items():
                if result:
                    print(f"✅ Form {test_name}: Present")
                else:
                    print(f"⚠️  Form {test_name}: Not detected")
                    
        except requests.exceptions.RequestException as e:
            self.test_results['forms'] = {'error': str(e)}
            print(f"❌ Form testing failed: {e}")
    
    def run_all_tests(self):
        """Run all simple tests"""
        print("Starting Simple Healthcare Dashboard Testing...")
        print("=" * 60)
        
        # Test server connectivity first
        if not self.test_server_connectivity():
            print("\n❌ Cannot proceed with testing - server is not running")
            print("Please start the Django server with: python manage.py runserver")
            return self.test_results
        
        # Run all other tests
        self.test_page_accessibility()
        self.test_static_files()
        self.test_mobile_responsiveness()
        self.test_ui_elements()
        self.test_form_accessibility()
        
        return self.test_results
    
    def generate_report(self):
        """Generate a simple test report"""
        print("\n" + "=" * 60)
        print("SIMPLE HEALTHCARE DASHBOARD TEST REPORT")
        print("=" * 60)
        
        # Calculate statistics
        total_tests = 0
        passed_tests = 0
        
        for category, tests in self.test_results.items():
            if isinstance(tests, dict):
                print(f"\n{category.upper()} TESTS:")
                print("-" * 30)
                
                for test_name, result in tests.items():
                    if isinstance(result, bool):
                        total_tests += 1
                        if result:
                            passed_tests += 1
                            print(f"  ✅ {test_name}")
                        else:
                            print(f"  ❌ {test_name}")
                    elif isinstance(result, (int, float)):
                        if test_name == 'load_time':
                            status = "✅" if result < 3.0 else "⚠️"
                            print(f"  {status} {test_name}: {result:.2f}s")
                        elif test_name == 'status_code':
                            status = "✅" if result in [200, 302] else "❌"
                            print(f"  {status} {test_name}: {result}")
                        else:
                            print(f"  ℹ️  {test_name}: {result}")
                    elif 'error' in str(result).lower():
                        print(f"  ❌ {test_name}: Error occurred")
        
        # Overall statistics
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"\n" + "=" * 60)
        print(f"OVERALL RESULTS:")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Recommendations
        print(f"\nRECOMMENDATIONS:")
        if success_rate >= 90:
            print("✅ Excellent! The healthcare dashboard is working well.")
        elif success_rate >= 70:
            print("⚠️  Good, but some improvements needed.")
        else:
            print("❌ Several issues found. Please review failed tests.")
        
        print("=" * 60)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f'simple_test_results_{timestamp}.json', 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        print(f"Results saved to: simple_test_results_{timestamp}.json")

if __name__ == "__main__":
    # Run the simple test suite
    test_suite = SimpleHealthcareTest()
    results = test_suite.run_all_tests()
    test_suite.generate_report()
