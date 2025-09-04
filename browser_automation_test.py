#!/usr/bin/env python3
"""
Browser Automation Testing for Healthcare Dashboard
Tests cross-platform compatibility, responsive design, and UI elements
"""

import os
import sys
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BrowserTestSuite:
    """Cross-platform browser testing suite"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_results = {
            'desktop': {},
            'mobile': {},
            'performance': {},
            'ui_elements': {},
            'responsive': {}
        }
        self.drivers = {}
    
    def setup_chrome_desktop(self):
        """Setup Chrome for desktop testing"""
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        # options.add_argument('--headless')  # Uncomment for headless testing
        
        try:
            driver = webdriver.Chrome(options=options)
            self.drivers['chrome_desktop'] = driver
            return driver
        except Exception as e:
            print(f"Failed to setup Chrome desktop: {e}")
            return None
    
    def setup_chrome_mobile(self):
        """Setup Chrome for mobile testing"""
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--headless')
        
        # Mobile emulation
        mobile_emulation = {
            "deviceMetrics": {"width": 375, "height": 667, "pixelRatio": 2.0},
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
        }
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        try:
            driver = webdriver.Chrome(options=options)
            self.drivers['chrome_mobile'] = driver
            return driver
        except Exception as e:
            print(f"Failed to setup Chrome mobile: {e}")
            return None
    
    def setup_firefox_desktop(self):
        """Setup Firefox for desktop testing"""
        options = FirefoxOptions()
        # options.add_argument('--headless')
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')
        
        try:
            driver = webdriver.Firefox(options=options)
            self.drivers['firefox_desktop'] = driver
            return driver
        except Exception as e:
            print(f"Failed to setup Firefox desktop: {e}")
            return None
    
    def test_login_functionality(self, driver, platform):
        """Test login functionality"""
        try:
            driver.get(f"{self.base_url}/accounts/login/")
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            # Find login elements
            username_field = driver.find_element(By.NAME, "username")
            password_field = driver.find_element(By.NAME, "password")
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            
            # Test form interaction
            username_field.send_keys("test_admin")
            password_field.send_keys("testpass123")
            
            # Check if elements are visible and clickable
            login_test = {
                'page_loads': True,
                'form_elements_present': True,
                'form_interactive': username_field.is_enabled() and password_field.is_enabled(),
                'button_clickable': login_button.is_enabled()
            }
            
            return login_test
            
        except Exception as e:
            return {'page_loads': False, 'error': str(e)}
    
    def test_dashboard_elements(self, driver, platform):
        """Test dashboard UI elements"""
        try:
            # Assuming we're logged in or can access dashboard
            driver.get(f"{self.base_url}/dashboard/")
            
            # Wait for dashboard to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dashboard-card"))
            )
            
            # Test various UI elements
            elements_test = {
                'dashboard_cards': len(driver.find_elements(By.CLASS_NAME, "dashboard-card")) > 0,
                'navigation_menu': len(driver.find_elements(By.CLASS_NAME, "nav-link")) > 0,
                'quick_actions': len(driver.find_elements(By.CLASS_NAME, "quick-action-btn")) > 0,
                'statistics_display': len(driver.find_elements(By.CLASS_NAME, "stat-card")) > 0,
                'responsive_layout': True  # Will be tested separately
            }
            
            # Test glassmorphism effects (check for backdrop-filter CSS)
            try:
                glass_elements = driver.find_elements(By.CSS_SELECTOR, "[style*='backdrop-filter']")
                elements_test['glassmorphism_effects'] = len(glass_elements) > 0
            except:
                elements_test['glassmorphism_effects'] = False
            
            # Test Ethiopian color scheme
            try:
                ethiopian_colors = driver.find_elements(By.CSS_SELECTOR, ".text-ethiopia-green, .text-ethiopia-blue, .text-ethiopia-yellow")
                elements_test['ethiopian_colors'] = len(ethiopian_colors) > 0
            except:
                elements_test['ethiopian_colors'] = False
            
            return elements_test
            
        except Exception as e:
            return {'dashboard_loads': False, 'error': str(e)}
    
    def test_module_navigation(self, driver, platform):
        """Test navigation between modules"""
        try:
            navigation_test = {}
            
            # Test navigation to each module
            modules = [
                ('patients', '/dashboard/'),
                ('appointments', '/appointments/'),
                ('doctors', '/doctors/'),
                ('pharmacy', '/pharmacy/'),
                ('billing', '/billing/')
            ]
            
            for module_name, url in modules:
                try:
                    driver.get(f"{self.base_url}{url}")
                    
                    # Wait for page to load
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    
                    # Check if page loaded successfully
                    navigation_test[f'{module_name}_loads'] = "error" not in driver.current_url.lower()
                    
                    # Check for module-specific elements
                    if module_name == 'patients':
                        navigation_test[f'{module_name}_elements'] = len(driver.find_elements(By.CSS_SELECTOR, ".patient-card, .add-patient-btn")) > 0
                    elif module_name == 'appointments':
                        navigation_test[f'{module_name}_elements'] = len(driver.find_elements(By.CSS_SELECTOR, ".appointment-card, .add-appointment-btn")) > 0
                    elif module_name == 'doctors':
                        navigation_test[f'{module_name}_elements'] = len(driver.find_elements(By.CSS_SELECTOR, ".doctor-card, .add-doctor-btn")) > 0
                    elif module_name == 'pharmacy':
                        navigation_test[f'{module_name}_elements'] = len(driver.find_elements(By.CSS_SELECTOR, ".medicine-card, .add-medicine-btn")) > 0
                    elif module_name == 'billing':
                        navigation_test[f'{module_name}_elements'] = len(driver.find_elements(By.CSS_SELECTOR, ".invoice-card, .add-invoice-btn")) > 0
                    
                except Exception as e:
                    navigation_test[f'{module_name}_loads'] = False
                    navigation_test[f'{module_name}_error'] = str(e)
            
            return navigation_test
            
        except Exception as e:
            return {'navigation_test': False, 'error': str(e)}
    
    def test_responsive_design(self, driver, platform):
        """Test responsive design at different breakpoints"""
        try:
            responsive_test = {}
            
            # Test different screen sizes
            breakpoints = [
                (1920, 1080, 'desktop_large'),
                (1366, 768, 'desktop_medium'),
                (1024, 768, 'tablet_landscape'),
                (768, 1024, 'tablet_portrait'),
                (375, 667, 'mobile_large'),
                (320, 568, 'mobile_small')
            ]
            
            for width, height, size_name in breakpoints:
                try:
                    driver.set_window_size(width, height)
                    time.sleep(1)  # Allow layout to adjust
                    
                    # Navigate to dashboard
                    driver.get(f"{self.base_url}/dashboard/")
                    
                    # Check if layout adapts properly
                    body = driver.find_element(By.TAG_NAME, "body")
                    responsive_test[f'{size_name}_layout'] = body.is_displayed()
                    
                    # Check for mobile-specific elements on small screens
                    if width <= 768:
                        mobile_nav = driver.find_elements(By.CLASS_NAME, "navbar-toggler")
                        responsive_test[f'{size_name}_mobile_nav'] = len(mobile_nav) > 0
                    
                    # Check for overflow issues
                    responsive_test[f'{size_name}_no_overflow'] = driver.execute_script(
                        "return document.body.scrollWidth <= window.innerWidth"
                    )
                    
                except Exception as e:
                    responsive_test[f'{size_name}_error'] = str(e)
            
            return responsive_test
            
        except Exception as e:
            return {'responsive_test': False, 'error': str(e)}
    
    def test_performance_metrics(self, driver, platform):
        """Test performance metrics"""
        try:
            performance_test = {}
            
            # Navigate to dashboard and measure load time
            start_time = time.time()
            driver.get(f"{self.base_url}/dashboard/")
            
            # Wait for page to be fully loaded
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dashboard-card"))
            )
            
            load_time = time.time() - start_time
            performance_test['page_load_time'] = load_time
            performance_test['load_time_acceptable'] = load_time < 5.0  # Under 5 seconds
            
            # Test JavaScript execution
            try:
                js_test = driver.execute_script("return typeof jQuery !== 'undefined' || typeof $ !== 'undefined';")
                performance_test['javascript_working'] = js_test
            except:
                performance_test['javascript_working'] = False
            
            # Test CSS loading
            try:
                css_test = driver.execute_script("""
                    var element = document.querySelector('.btn');
                    if (element) {
                        var styles = window.getComputedStyle(element);
                        return styles.backgroundColor !== 'rgba(0, 0, 0, 0)';
                    }
                    return false;
                """)
                performance_test['css_loaded'] = css_test
            except:
                performance_test['css_loaded'] = False
            
            return performance_test
            
        except Exception as e:
            return {'performance_test': False, 'error': str(e)}
    
    def run_comprehensive_tests(self):
        """Run all tests across different browsers and platforms"""
        print("Starting Comprehensive Browser Testing...")
        print("=" * 60)
        
        # Setup browsers
        browsers = [
            ('chrome_desktop', self.setup_chrome_desktop),
            ('chrome_mobile', self.setup_chrome_mobile),
            ('firefox_desktop', self.setup_firefox_desktop)
        ]
        
        for browser_name, setup_func in browsers:
            print(f"\nTesting {browser_name}...")
            driver = setup_func()
            
            if driver:
                try:
                    # Run all test suites
                    platform = 'mobile' if 'mobile' in browser_name else 'desktop'
                    
                    self.test_results[platform][f'{browser_name}_login'] = self.test_login_functionality(driver, platform)
                    self.test_results[platform][f'{browser_name}_dashboard'] = self.test_dashboard_elements(driver, platform)
                    self.test_results[platform][f'{browser_name}_navigation'] = self.test_module_navigation(driver, platform)
                    self.test_results['responsive'][browser_name] = self.test_responsive_design(driver, platform)
                    self.test_results['performance'][browser_name] = self.test_performance_metrics(driver, platform)
                    
                    print(f"✅ {browser_name} tests completed")
                    
                except Exception as e:
                    print(f"❌ {browser_name} tests failed: {e}")
                    self.test_results[platform][f'{browser_name}_error'] = str(e)
                
                finally:
                    driver.quit()
            else:
                print(f"❌ Failed to setup {browser_name}")
        
        return self.test_results
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("COMPREHENSIVE BROWSER TESTING REPORT")
        print("=" * 60)
        
        # Calculate overall statistics
        total_tests = 0
        passed_tests = 0
        
        for platform, browsers in self.test_results.items():
            if isinstance(browsers, dict):
                print(f"\n{platform.upper()} TESTING:")
                print("-" * 40)
                
                for browser, tests in browsers.items():
                    if isinstance(tests, dict):
                        print(f"\n  {browser}:")
                        for test_name, result in tests.items():
                            if isinstance(result, bool):
                                total_tests += 1
                                if result:
                                    passed_tests += 1
                                    print(f"    ✅ {test_name}")
                                else:
                                    print(f"    ❌ {test_name}")
                            elif isinstance(result, dict):
                                for sub_test, sub_result in result.items():
                                    if isinstance(sub_result, bool):
                                        total_tests += 1
                                        if sub_result:
                                            passed_tests += 1
                                            print(f"    ✅ {sub_test}")
                                        else:
                                            print(f"    ❌ {sub_test}")
        
        # Overall statistics
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"\n" + "=" * 60)
        print(f"OVERALL RESULTS:")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print("=" * 60)
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f'browser_test_results_{timestamp}.json', 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        print(f"Detailed results saved to: browser_test_results_{timestamp}.json")

if __name__ == "__main__":
    # Run the comprehensive browser test suite
    test_suite = BrowserTestSuite()
    results = test_suite.run_comprehensive_tests()
    test_suite.generate_report()
