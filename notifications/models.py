from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    """Notification model for system-wide notifications"""
    
    NOTIFICATION_TYPES = [
        ('appointment', 'Appointment'),
        ('patient', 'Patient'),
        ('billing', 'Billing'),
        ('pharmacy', 'Pharmacy'),
        ('system', 'System'),
        ('reminder', 'Reminder'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Core Fields
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='system')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    
    # Recipients
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Optional Links
    action_url = models.URLField(blank=True, help_text="URL to redirect when notification is clicked")
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
    
    def get_icon(self):
        """Get appropriate icon for notification type"""
        icons = {
            'appointment': 'fas fa-calendar-alt',
            'patient': 'fas fa-user-plus',
            'billing': 'fas fa-file-invoice',
            'pharmacy': 'fas fa-pills',
            'system': 'fas fa-cog',
            'reminder': 'fas fa-bell',
        }
        return icons.get(self.notification_type, 'fas fa-info-circle')
    
    def get_color_class(self):
        """Get appropriate color class for notification priority"""
        colors = {
            'low': 'text-muted',
            'normal': 'text-primary',
            'high': 'text-warning',
            'urgent': 'text-danger',
        }
        return colors.get(self.priority, 'text-primary')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"


class NotificationPreference(models.Model):
    """User notification preferences"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Email Notifications
    email_appointments = models.BooleanField(default=True)
    email_patients = models.BooleanField(default=True)
    email_billing = models.BooleanField(default=True)
    email_pharmacy = models.BooleanField(default=True)
    email_system = models.BooleanField(default=True)
    
    # In-App Notifications
    app_appointments = models.BooleanField(default=True)
    app_patients = models.BooleanField(default=True)
    app_billing = models.BooleanField(default=True)
    app_pharmacy = models.BooleanField(default=True)
    app_system = models.BooleanField(default=True)
    
    # SMS Notifications (for future implementation)
    sms_appointments = models.BooleanField(default=False)
    sms_urgent_only = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Notification preferences for {self.user.username}"
    
    class Meta:
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'
