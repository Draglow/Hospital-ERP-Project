"""
Context processors for Ethiopian Hospital ERP
"""

def mobile_context(request):
    """
    Add mobile context to all templates
    """
    is_mobile_request = request.GET.get('mobile') == '1'
    
    # Also check user agent for mobile devices
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    is_mobile_device = any(device in user_agent for device in [
        'mobile', 'android', 'iphone', 'ipad', 'ipod', 'blackberry', 'windows phone'
    ])
    
    return {
        'is_mobile_request': is_mobile_request,
        'is_mobile_device': is_mobile_device,
        'use_mobile_template': is_mobile_request or (is_mobile_device and not request.GET.get('desktop')),
        'mobile_base_template': 'dashboard/mobile/base.html' if (is_mobile_request or is_mobile_device) else 'dashboard/base.html'
    }
