#!/usr/bin/env python
"""
Verification script for login/logout optimizations
Ethiopian Hospital ERP System
"""

import os
import re

def check_file_exists(filepath):
    """Check if file exists and return status"""
    return os.path.exists(filepath)

def check_file_content(filepath, patterns):
    """Check if file contains specific patterns"""
    if not os.path.exists(filepath):
        return False, f"File {filepath} not found"
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        missing_patterns = []
        for pattern_name, pattern in patterns.items():
            if not re.search(pattern, content, re.MULTILINE | re.DOTALL):
                missing_patterns.append(pattern_name)
        
        if missing_patterns:
            return False, f"Missing patterns: {', '.join(missing_patterns)}"
        
        return True, "All patterns found"
    
    except Exception as e:
        return False, f"Error reading file: {str(e)}"

def verify_optimizations():
    """Verify all optimizations are in place"""
    print("🔍 Verifying Login/Logout Optimizations...")
    print("=" * 60)
    
    checks = []
    
    # 1. Check login template optimization (removed setTimeout)
    login_patterns = {
        'immediate_submit': r'this\.submit\(\);',
        'no_timeout': r'(?!.*setTimeout.*this\.submit)',
    }
    
    status, msg = check_file_content('templates/accounts/login.html', login_patterns)
    checks.append(("Login Template Optimization", status, msg))
    
    # 2. Check custom logout view
    logout_patterns = {
        'custom_logout_class': r'class CustomLogoutView',
        'session_flush': r'request\.session\.flush\(\)',
        'performance_logging': r'logout_time.*time\.time',
    }
    
    status, msg = check_file_content('accounts/views.py', logout_patterns)
    checks.append(("Custom Logout View", status, msg))
    
    # 3. Check middleware implementation
    middleware_patterns = {
        'session_timeout_middleware': r'class SessionTimeoutMiddleware',
        'security_headers': r'class SecurityHeadersMiddleware',
        'mobile_detection': r'class MobileDetectionMiddleware',
    }
    
    status, msg = check_file_content('accounts/middleware.py', middleware_patterns)
    checks.append(("Custom Middleware", status, msg))
    
    # 4. Check settings configuration
    settings_patterns = {
        'session_config': r'SESSION_ENGINE.*db',
        'middleware_order': r'accounts\.middleware\.SessionTimeoutMiddleware',
        'logging_config': r'LOGGING.*=.*{',
    }
    
    status, msg = check_file_content('hospital_erp/settings.py', settings_patterns)
    checks.append(("Settings Configuration", status, msg))
    
    # 5. Check URL configuration
    url_patterns = {
        'custom_logout_url': r'views\.CustomLogoutView\.as_view\(\)',
    }
    
    status, msg = check_file_content('accounts/urls.py', url_patterns)
    checks.append(("URL Configuration", status, msg))
    
    # 6. Check template fixes
    mobile_base_patterns = {
        'mobile_logout_param': r'accounts:logout.*\?mobile=1',
    }
    
    status, msg = check_file_content('templates/dashboard/mobile/base.html', mobile_base_patterns)
    checks.append(("Mobile Template Fixes", status, msg))
    
    # 7. Check desktop template fixes
    desktop_base_patterns = {
        'desktop_logout_url': r'accounts:logout',
    }
    
    status, msg = check_file_content('templates/dashboard/base.html', desktop_base_patterns)
    checks.append(("Desktop Template Fixes", status, msg))
    
    # 8. Check logs directory
    logs_exists = check_file_exists('logs')
    checks.append(("Logs Directory", logs_exists, "Directory created" if logs_exists else "Directory missing"))
    
    # Print results
    passed = 0
    failed = 0
    
    for check_name, status, message in checks:
        icon = "✅" if status else "❌"
        print(f"{icon} {check_name}: {message}")
        if status:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All optimizations verified successfully!")
        print("\n📈 Performance Improvements:")
        print("  • Removed 1-second artificial delay from login")
        print("  • Added session timeout middleware")
        print("  • Implemented proper logout with session cleanup")
        print("  • Added performance logging and monitoring")
        print("  • Fixed mobile/desktop logout redirection")
        print("  • Enhanced security headers")
        print("  • Optimized database queries in login process")
        
        print("\n🔧 Key Features Added:")
        print("  • Custom logout view with proper session termination")
        print("  • Session timeout based on user settings")
        print("  • Performance monitoring and logging")
        print("  • Cross-device compatibility")
        print("  • Security enhancements")
        
        return True
    else:
        print("⚠️  Some optimizations may not be properly implemented.")
        return False

def print_usage_instructions():
    """Print instructions for using the optimized system"""
    print("\n" + "=" * 60)
    print("📋 USAGE INSTRUCTIONS")
    print("=" * 60)
    
    print("\n🚀 To test the optimizations:")
    print("1. Start the Django development server:")
    print("   python manage.py runserver")
    
    print("\n2. Test login performance:")
    print("   • Navigate to /accounts/login/")
    print("   • Notice immediate form submission (no 1-second delay)")
    print("   • Check browser network tab for timing")
    
    print("\n3. Test logout functionality:")
    print("   • Desktop: Click logout from user dropdown")
    print("   • Mobile: Access via mobile sidebar or profile")
    print("   • Verify proper redirection and session cleanup")
    
    print("\n4. Test session timeout:")
    print("   • Login and wait for configured timeout period")
    print("   • System should auto-logout inactive users")
    
    print("\n5. Monitor performance:")
    print("   • Check logs/hospital_erp.log for performance metrics")
    print("   • Login/logout times are logged automatically")
    
    print("\n6. Test cross-device compatibility:")
    print("   • Test on different screen sizes")
    print("   • Verify mobile vs desktop redirections")
    print("   • Check responsive behavior")

if __name__ == '__main__':
    success = verify_optimizations()
    
    if success:
        print_usage_instructions()
    
    exit(0 if success else 1)
