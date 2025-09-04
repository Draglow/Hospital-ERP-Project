"""
Custom middleware for Ethiopian Hospital ERP
"""
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class SessionTimeoutMiddleware:
    """
    Middleware to handle session timeout based on user settings
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip timeout check for certain URLs
        skip_urls = [
            '/accounts/login/',
            '/accounts/logout/',
            '/static/',
            '/media/',
            '/admin/',
        ]
        
        if any(request.path.startswith(url) for url in skip_urls):
            return self.get_response(request)
        
        # Only check timeout for authenticated users
        if request.user.is_authenticated:
            self.check_session_timeout(request)
        
        response = self.get_response(request)
        
        # Update last activity timestamp
        if request.user.is_authenticated:
            request.session['last_activity'] = timezone.now().isoformat()
        
        return response
    
    def check_session_timeout(self, request):
        """Check if session has timed out based on user settings"""
        try:
            # Get user's session timeout setting (default to 60 minutes)
            timeout_minutes = 60
            try:
                if hasattr(request.user, 'settings') and request.user.settings:
                    timeout_minutes = request.user.settings.session_timeout
            except Exception:
                # If user settings don't exist, use default
                pass
            
            # Get last activity from session
            last_activity_str = request.session.get('last_activity')
            if not last_activity_str:
                # First time - set current time
                request.session['last_activity'] = timezone.now().isoformat()
                return
            
            # Parse last activity time
            try:
                last_activity = timezone.datetime.fromisoformat(last_activity_str)
                if last_activity.tzinfo is None:
                    last_activity = timezone.make_aware(last_activity)
            except ValueError:
                # If parsing fails, reset to current time
                request.session['last_activity'] = timezone.now().isoformat()
                return
            
            # Check if session has expired
            timeout_delta = timedelta(minutes=timeout_minutes)
            if timezone.now() - last_activity > timeout_delta:
                # Session expired - logout user
                user_name = request.user.get_full_name() or request.user.username
                logout(request)
                messages.warning(
                    request, 
                    f'Your session has expired after {timeout_minutes} minutes of inactivity. Please log in again.'
                )
                logger.info(f'Session timeout for user: {user_name}')
                
        except Exception as e:
            # Log error but don't break the request
            logger.error(f'Error in session timeout check: {str(e)}')


class SecurityHeadersMiddleware:
    """
    Middleware to add security headers
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Add CSP header for login page
        if request.path == '/accounts/login/':
            response['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
                "img-src 'self' data: https:; "
                "font-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
                "connect-src 'self';"
            )
        
        return response


class MobileDetectionMiddleware:
    """
    Middleware to enhance mobile detection and add context
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Enhanced mobile detection
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        mobile_keywords = [
            'mobile', 'android', 'iphone', 'ipad', 'ipod', 
            'blackberry', 'windows phone', 'opera mini'
        ]
        
        request.is_mobile_device = any(keyword in user_agent for keyword in mobile_keywords)
        request.is_mobile_request = request.GET.get('mobile') == '1'
        request.force_desktop = request.GET.get('desktop') == '1'
        
        # Determine if mobile template should be used
        request.use_mobile_template = (
            (request.is_mobile_request or request.is_mobile_device) 
            and not request.force_desktop
        )
        
        return self.get_response(request)
