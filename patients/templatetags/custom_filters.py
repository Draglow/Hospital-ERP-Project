from django import template
from datetime import date, timedelta
from decimal import Decimal

register = template.Library()

@register.filter
def days_until(value):
    """Calculate days until a given date"""
    if not value:
        return 0
    
    if isinstance(value, str):
        return 0
    
    today = date.today()
    if hasattr(value, 'date'):
        value = value.date()
    
    delta = value - today
    return delta.days

@register.filter
def mul(value, arg):
    """Multiply two values"""
    try:
        if value is None or arg is None:
            return 0
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def age_from_birthdate(birthdate):
    """Calculate age from birthdate"""
    if not birthdate:
        return 0
    
    today = date.today()
    if hasattr(birthdate, 'date'):
        birthdate = birthdate.date()
    
    age = today.year - birthdate.year
    if today.month < birthdate.month or (today.month == birthdate.month and today.day < birthdate.day):
        age -= 1
    
    return age

@register.filter
def ethiopian_date(value):
    """Format date in Ethiopian style"""
    if not value:
        return ""
    
    if hasattr(value, 'strftime'):
        return value.strftime("%B %d, %Y")
    
    return str(value)

@register.filter
def currency_format(value):
    """Format currency in Ethiopian Birr"""
    try:
        if value is None:
            return "0.00 ETB"
        return f"{float(value):,.2f} ETB"
    except (ValueError, TypeError):
        return "0.00 ETB"

@register.filter
def percentage(value, total):
    """Calculate percentage"""
    try:
        if not total or total == 0:
            return 0
        return round((float(value) / float(total)) * 100, 1)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def status_badge_class(status):
    """Return Bootstrap badge class for status"""
    status_classes = {
        'active': 'bg-success',
        'inactive': 'bg-secondary',
        'pending': 'bg-warning',
        'cancelled': 'bg-danger',
        'completed': 'bg-primary',
        'scheduled': 'bg-info',
        'confirmed': 'bg-success',
        'in_progress': 'bg-warning',
        'expired': 'bg-danger',
        'low_stock': 'bg-warning',
        'out_of_stock': 'bg-danger',
        'available': 'bg-success',
    }
    return status_classes.get(status.lower() if status else '', 'bg-secondary')

@register.filter
def priority_class(priority):
    """Return CSS class for priority levels"""
    priority_classes = {
        'high': 'text-danger',
        'medium': 'text-warning',
        'low': 'text-info',
        'urgent': 'text-danger',
        'normal': 'text-primary',
    }
    return priority_classes.get(priority.lower() if priority else '', 'text-secondary')

@register.filter
def truncate_smart(value, length=50):
    """Smart truncation that preserves word boundaries"""
    if not value or len(value) <= length:
        return value
    
    truncated = value[:length]
    last_space = truncated.rfind(' ')
    
    if last_space > length * 0.8:  # If last space is reasonably close to end
        return truncated[:last_space] + '...'
    else:
        return truncated + '...'

@register.filter
def phone_format(value):
    """Format phone number in Ethiopian format"""
    if not value:
        return ""
    
    # Remove any non-digit characters
    digits = ''.join(filter(str.isdigit, str(value)))
    
    # Ethiopian phone number formatting
    if len(digits) == 10 and digits.startswith('9'):
        return f"+251 {digits[0]} {digits[1:3]} {digits[3:6]} {digits[6:]}"
    elif len(digits) == 9:
        return f"+251 9 {digits[0:2]} {digits[2:5]} {digits[5:]}"
    else:
        return value

@register.filter
def medical_priority(value):
    """Determine medical priority level"""
    if not value:
        return 'normal'
    
    value_str = str(value).lower()
    if any(word in value_str for word in ['emergency', 'urgent', 'critical', 'severe']):
        return 'high'
    elif any(word in value_str for word in ['important', 'moderate', 'follow-up']):
        return 'medium'
    else:
        return 'low'

@register.filter
def time_ago(value):
    """Human readable time ago"""
    if not value:
        return ""
    
    from django.utils import timezone
    
    now = timezone.now()
    if hasattr(value, 'replace'):
        if value.tzinfo is None:
            value = timezone.make_aware(value)
    
    diff = now - value
    
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "Just now"

@register.filter
def stock_level_class(current, minimum):
    """Return CSS class based on stock level"""
    try:
        current = float(current or 0)
        minimum = float(minimum or 0)
        
        if current == 0:
            return 'text-danger'
        elif current <= minimum:
            return 'text-warning'
        elif current <= minimum * 1.5:
            return 'text-info'
        else:
            return 'text-success'
    except (ValueError, TypeError):
        return 'text-secondary'

@register.filter
def expiry_status(expiry_date):
    """Determine expiry status"""
    if not expiry_date:
        return 'unknown'
    
    today = date.today()
    if hasattr(expiry_date, 'date'):
        expiry_date = expiry_date.date()
    
    days_left = (expiry_date - today).days
    
    if days_left < 0:
        return 'expired'
    elif days_left <= 7:
        return 'critical'
    elif days_left <= 30:
        return 'warning'
    else:
        return 'good'

@register.filter
def boolean_icon(value):
    """Return icon for boolean values"""
    if value:
        return '<i class="fas fa-check-circle text-success"></i>'
    else:
        return '<i class="fas fa-times-circle text-danger"></i>'

@register.filter
def list_to_string(value, separator=', '):
    """Convert list to string with separator"""
    if not value:
        return ""
    
    if isinstance(value, (list, tuple)):
        return separator.join(str(item) for item in value)
    
    return str(value)
