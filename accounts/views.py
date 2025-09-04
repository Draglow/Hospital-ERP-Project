from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import views as auth_views, logout
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.utils import timezone
from .models import UserSettings
import json
import logging
import time

logger = logging.getLogger(__name__)

@login_required
def profile_view(request):
    """User profile view with mobile template support"""
    if request.method == 'POST':
        # Handle profile update
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')

        # Handle phone if the field exists
        if hasattr(user, 'phone'):
            user.phone = request.POST.get('phone', '')

        # Handle profile image if uploaded
        if 'profile_image' in request.FILES:
            if hasattr(user, 'profile_image'):
                user.profile_image = request.FILES['profile_image']

        user.save()
        messages.success(request, 'Profile updated successfully!')

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'accounts/mobile_profile.html' if is_mobile else 'accounts/profile.html'

    return render(request, template_name, {'user': request.user})

@login_required
def settings_view(request):
    """User settings view with mobile template support"""
    # Get or create user settings
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'accounts/mobile_settings.html' if is_mobile else 'accounts/settings.html'

    context = {
        'user': request.user,
        'settings': user_settings,
        'language_choices': UserSettings.LANGUAGE_CHOICES,
        'date_format_choices': UserSettings.DATE_FORMAT_CHOICES,
        'session_timeout_choices': UserSettings.SESSION_TIMEOUT_CHOICES,
    }

    return render(request, template_name, context)


class CustomLoginView(auth_views.LoginView):
    """Custom login view with mobile detection and appropriate redirect"""
    template_name = 'accounts/login.html'

    def get_success_url(self):
        """Redirect to mobile dashboard if mobile device detected, otherwise desktop dashboard"""
        # Check if mobile parameter is present in the request
        is_mobile_request = self.request.GET.get('mobile') == '1'

        # Check user agent for mobile devices
        user_agent = self.request.META.get('HTTP_USER_AGENT', '').lower()
        is_mobile_device = any(device in user_agent for device in [
            'mobile', 'android', 'iphone', 'ipad', 'ipod', 'blackberry', 'windows phone'
        ])

        # Check if user explicitly requested desktop version
        force_desktop = self.request.GET.get('desktop') == '1'

        # Determine redirect URL
        if (is_mobile_request or is_mobile_device) and not force_desktop:
            return reverse('patients:mobile_dashboard')
        else:
            return reverse('patients:dashboard')

    def form_valid(self, form):
        """Override to handle mobile redirect and remember me functionality"""
        start_time = time.time()

        response = super().form_valid(form)

        # Handle "Remember Me" functionality
        remember_me = self.request.POST.get('remember_me')
        if remember_me:
            # Set session to expire when browser closes (default) or extend it
            # If remember me is checked, extend session to 30 days
            self.request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days in seconds
        else:
            # Set session to expire when browser closes
            self.request.session.set_expiry(0)

        # Optimize user display name - avoid extra database queries
        user = self.request.user
        display_name = user.get_full_name() if (user.first_name or user.last_name) else user.username

        # Add a success message
        messages.success(self.request, f'Welcome back, {display_name}!')

        # Log login performance
        login_time = time.time() - start_time
        logger.info(f'Login successful for user {user.username} in {login_time:.3f}s')

        # Store login timestamp for session management
        self.request.session['login_time'] = timezone.now().isoformat()
        self.request.session['last_activity'] = timezone.now().isoformat()

        return response


@method_decorator(never_cache, name='dispatch')
class CustomLogoutView(auth_views.LogoutView):
    """Custom logout view with proper session cleanup and mobile detection"""

    # Allow both GET and POST requests for logout
    http_method_names = ['get', 'post', 'options']

    # Force redirect to homepage
    next_page = '/'

    def dispatch(self, request, *args, **kwargs):
        """Handle logout with proper session cleanup"""
        start_time = time.time()
        logger.info(f'CustomLogoutView.dispatch called - URL: {request.path}, Method: {request.method}')

        if request.user.is_authenticated:
            # Log logout attempt
            user_name = request.user.get_full_name() or request.user.username
            username = request.user.username

            # Calculate session duration if available
            login_time_str = request.session.get('login_time')
            session_duration = None
            if login_time_str:
                try:
                    login_time = timezone.datetime.fromisoformat(login_time_str)
                    if login_time.tzinfo is None:
                        login_time = timezone.make_aware(login_time)
                    session_duration = (timezone.now() - login_time).total_seconds()
                except Exception:
                    pass

            # Add logout message before logging out
            messages.success(request, f'You have been successfully logged out. Goodbye, {user_name}!')

            # Log logout performance
            logout_time = time.time() - start_time
            if session_duration:
                logger.info(f'Logout successful for user {username} in {logout_time:.3f}s (session duration: {session_duration:.1f}s)')
            else:
                logger.info(f'Logout successful for user {username} in {logout_time:.3f}s')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Handle GET requests for logout (for backward compatibility)"""
        return self.post(request, *args, **kwargs)

    def get_next_page(self):
        """Determine redirect URL based on device type - redirect to homepage"""
        # Always redirect to homepage after logout
        homepage_url = '/'
        logger.info(f'CustomLogoutView redirecting to: {homepage_url}')
        return homepage_url


@csrf_exempt
def simple_logout_view(request):
    """Simple function-based logout view that definitely redirects to homepage"""
    if request.user.is_authenticated:
        user_name = request.user.get_full_name() or request.user.username
        messages.success(request, f'You have been successfully logged out. Goodbye, {user_name}!')
        logger.info(f'Simple logout for user: {request.user.username}')
        logout(request)

    logger.info('Simple logout redirecting to homepage: /')
    return HttpResponseRedirect('/')


def debug_logout_view(request):
    """Debug view to test logout functionality"""
    context = {
        'user_authenticated': request.user.is_authenticated,
        'user_name': request.user.username if request.user.is_authenticated else 'Anonymous',
        'request_method': request.method,
        'request_path': request.path,
        'logout_url': reverse('accounts:logout'),
        'homepage_url': reverse('homepage'),
    }
    return render(request, 'logout_debug.html', context)


@login_required
@require_POST
def save_settings(request):
    """Save user settings via AJAX"""
    try:
        # Get or create user settings
        user_settings, created = UserSettings.objects.get_or_create(user=request.user)

        # Parse JSON data from request body
        data = json.loads(request.body)

        # Update basic settings
        if 'two_factor_enabled' in data:
            user_settings.two_factor_enabled = data['two_factor_enabled']
        if 'email_notifications' in data:
            user_settings.email_notifications = data['email_notifications']
        if 'push_notifications' in data:
            user_settings.push_notifications = data['push_notifications']
        if 'appointment_reminders' in data:
            user_settings.appointment_reminders = data['appointment_reminders']
        if 'language' in data:
            user_settings.language = data['language']
        if 'date_format' in data:
            user_settings.date_format = data['date_format']
        if 'session_timeout' in data:
            user_settings.session_timeout = int(data['session_timeout'])

        # Update additional settings
        if 'additional_settings' in data:
            for key, value in data['additional_settings'].items():
                user_settings.set_setting(key, value)

        user_settings.save()

        return JsonResponse({
            'success': True,
            'message': 'Settings saved successfully!'
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error saving settings: {str(e)}'
        }, status=500)


@login_required
def get_settings(request):
    """Get user settings as JSON"""
    try:
        user_settings, created = UserSettings.objects.get_or_create(user=request.user)

        return JsonResponse({
            'success': True,
            'settings': user_settings.get_all_settings()
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error retrieving settings: {str(e)}'
        }, status=500)


@login_required
@require_POST
def reset_settings(request):
    """Reset user settings to defaults"""
    try:
        user_settings, created = UserSettings.objects.get_or_create(user=request.user)

        # Reset to default values
        user_settings.two_factor_enabled = False
        user_settings.email_notifications = True
        user_settings.push_notifications = False
        user_settings.appointment_reminders = True
        user_settings.language = 'en'
        user_settings.date_format = 'gregorian'
        user_settings.session_timeout = 60
        user_settings.additional_settings = {}

        user_settings.save()

        return JsonResponse({
            'success': True,
            'message': 'Settings reset to defaults successfully!'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error resetting settings: {str(e)}'
        }, status=500)


@login_required
def settings_test_view(request):
    """Mobile settings test page"""
    return render(request, 'accounts/mobile_settings_test.html')
