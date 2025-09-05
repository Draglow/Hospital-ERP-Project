from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Notification, NotificationPreference


@login_required
def notification_list(request):
    """List all notifications for the current user"""
    notifications = Notification.objects.filter(recipient=request.user)

    # Filter by read status
    status_filter = request.GET.get('status', '')
    if status_filter == 'unread':
        notifications = notifications.filter(is_read=False)
    elif status_filter == 'read':
        notifications = notifications.filter(is_read=True)

    # Filter by type
    type_filter = request.GET.get('type', '')
    if type_filter:
        notifications = notifications.filter(notification_type=type_filter)

    # Filter by priority
    priority_filter = request.GET.get('priority', '')
    if priority_filter:
        notifications = notifications.filter(priority=priority_filter)

    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        notifications = notifications.filter(
            Q(title__icontains=search_query) |
            Q(message__icontains=search_query)
        )

    # Sorting
    sort_by = request.GET.get('sort', 'date_desc')
    if sort_by == 'date_asc':
        notifications = notifications.order_by('created_at')
    elif sort_by == 'priority':
        # Custom ordering for priority: urgent, high, normal, low
       priority_order = ['urgent', 'high', 'normal', 'low']

       case_statement = " ".join([f"WHEN '{p}' THEN {i}" for i, p in enumerate(priority_order)])

       notifications = notifications.extra(
        select={'priority_order': f"CASE priority {case_statement} END"}
       ).order_by('priority_order', '-created_at')

    elif sort_by == 'type':
        notifications = notifications.order_by('notification_type', '-created_at')
    elif sort_by == 'unread_first':
        notifications = notifications.order_by('is_read', '-created_at')
    else:  # default: date_desc
        notifications = notifications.order_by('-created_at')

    # Pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'priority_filter': priority_filter,
        'search_query': search_query,
        'sort_by': sort_by,
        'notification_types': Notification.NOTIFICATION_TYPES,
        'priority_choices': Notification.PRIORITY_CHOICES,
        'unread_count': Notification.objects.filter(recipient=request.user, is_read=False).count(),
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'notifications/mobile_list.html' if is_mobile else 'notifications/list.html'

    return render(request, template_name, context)


@login_required
def notification_dropdown(request):
    """Get recent notifications for dropdown"""
    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')[:10]
    
    unread_count = Notification.objects.filter(
        recipient=request.user, 
        is_read=False
    ).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'notifications/dropdown.html', context)


@login_required
@require_POST
def mark_as_read(request, pk):
    """Mark a notification as read"""
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.mark_as_read()
    
    return JsonResponse({
        'success': True,
        'message': 'Notification marked as read'
    })


@login_required
@require_POST
def mark_all_as_read(request):
    """Mark all notifications as read for the current user"""
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(is_read=True)

    return JsonResponse({
        'success': True,
        'message': f'{count} notifications marked as read'
    })


@login_required
@require_POST
def delete_notification(request, pk):
    """Delete a notification"""
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification_title = notification.title
    notification.delete()

    return JsonResponse({
        'success': True,
        'message': f'Notification "{notification_title}" deleted successfully'
    })


@login_required
def notification_list_debug(request):
    """Debug version of notification list for testing delete functionality"""
    return render(request, 'notifications/list_standalone.html')


@login_required
def notification_preferences(request):
    """Manage notification preferences"""
    preferences, created = NotificationPreference.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        # Update preferences
        preferences.email_appointments = request.POST.get('email_appointments') == 'on'
        preferences.email_patients = request.POST.get('email_patients') == 'on'
        preferences.email_billing = request.POST.get('email_billing') == 'on'
        preferences.email_pharmacy = request.POST.get('email_pharmacy') == 'on'
        preferences.email_system = request.POST.get('email_system') == 'on'

        preferences.app_appointments = request.POST.get('app_appointments') == 'on'
        preferences.app_patients = request.POST.get('app_patients') == 'on'
        preferences.app_billing = request.POST.get('app_billing') == 'on'
        preferences.app_pharmacy = request.POST.get('app_pharmacy') == 'on'
        preferences.app_system = request.POST.get('app_system') == 'on'

        preferences.sms_appointments = request.POST.get('sms_appointments') == 'on'
        preferences.sms_urgent_only = request.POST.get('sms_urgent_only') == 'on'

        preferences.save()

        return JsonResponse({
            'success': True,
            'message': 'Notification preferences updated successfully'
        })

    context = {
        'preferences': preferences,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'notifications/mobile_preferences.html' if is_mobile else 'notifications/preferences.html'

    return render(request, template_name, context)


@login_required
def mobile_text_length_test(request):
    """Test page for mobile notification text length standardization"""
    return render(request, 'notifications/mobile_text_length_test.html')


@login_required
def mobile_action_buttons_test(request):
    """Test page for mobile notification action buttons functionality"""
    return render(request, 'notifications/mobile_action_buttons_test.html')
