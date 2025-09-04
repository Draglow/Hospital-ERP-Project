from .models import Notification


def notification_context(request):
    """Add notification context to all templates"""
    context = {
        'unread_notifications_count': 0,
    }
    
    if request.user.is_authenticated:
        try:
            context['unread_notifications_count'] = Notification.objects.filter(
                recipient=request.user,
                is_read=False
            ).count()
        except:
            # In case notifications table doesn't exist yet
            context['unread_notifications_count'] = 0
    
    return context
