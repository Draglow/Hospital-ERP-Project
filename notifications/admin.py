from django.contrib import admin
from .models import Notification, NotificationPreference


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'recipient', 'notification_type', 'priority', 'is_read', 'created_at']
    list_filter = ['notification_type', 'priority', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'recipient__username', 'recipient__email']
    readonly_fields = ['created_at', 'updated_at', 'read_at']
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('title', 'message', 'notification_type', 'priority')
        }),
        ('Recipients', {
            'fields': ('recipient', 'sender')
        }),
        ('Status', {
            'fields': ('is_read', 'read_at', 'action_url')
        }),
        ('System Info', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_appointments', 'app_appointments', 'sms_appointments']
    list_filter = ['email_appointments', 'app_appointments', 'sms_appointments']
    search_fields = ['user__username', 'user__email']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Email Notifications', {
            'fields': ('email_appointments', 'email_patients', 'email_billing', 'email_pharmacy', 'email_system')
        }),
        ('In-App Notifications', {
            'fields': ('app_appointments', 'app_patients', 'app_billing', 'app_pharmacy', 'app_system')
        }),
        ('SMS Notifications', {
            'fields': ('sms_appointments', 'sms_urgent_only')
        }),
    )
