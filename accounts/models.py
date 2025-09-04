from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import json

class User(AbstractUser):
    """Extended User model with Ethiopian context and role-based access"""

    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('receptionist', 'Receptionist'),
        ('pharmacist', 'Pharmacist'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='receptionist')
    phone_regex = RegexValidator(
        regex=r'^\+?251?[0-9]{9,10}$',
        message="Phone number must be entered in the format: '+251912345678' or '0912345678'. Up to 10 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=17, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    class Meta:
        db_table = 'auth_user'


class UserSettings(models.Model):
    """Model to store user preferences and settings"""

    # Language choices
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('am', 'አማርኛ'),
        ('or', 'Oromiffa'),
    ]

    # Date format choices
    DATE_FORMAT_CHOICES = [
        ('gregorian', 'Gregorian'),
        ('ethiopian', 'Ethiopian'),
    ]

    # Session timeout choices (in minutes)
    SESSION_TIMEOUT_CHOICES = [
        (30, '30 minutes'),
        (60, '1 hour'),
        (120, '2 hours'),
        (240, '4 hours'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')

    # Account Settings
    two_factor_enabled = models.BooleanField(default=False)

    # Notification Settings
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=False)
    appointment_reminders = models.BooleanField(default=True)

    # Display Settings
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    date_format = models.CharField(max_length=10, choices=DATE_FORMAT_CHOICES, default='gregorian')
    timezone = models.CharField(max_length=50, default='Africa/Addis_Ababa')

    # Privacy & Security Settings
    session_timeout = models.IntegerField(choices=SESSION_TIMEOUT_CHOICES, default=60)

    # Additional settings stored as JSON for flexibility
    additional_settings = models.JSONField(default=dict, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Settings'
        verbose_name_plural = 'User Settings'

    def __str__(self):
        return f"Settings for {self.user.username}"

    def get_setting(self, key, default=None):
        """Get a setting from additional_settings JSON field"""
        return self.additional_settings.get(key, default)

    def set_setting(self, key, value):
        """Set a setting in additional_settings JSON field"""
        self.additional_settings[key] = value
        self.save()

    def get_all_settings(self):
        """Return all settings as a dictionary"""
        return {
            'two_factor_enabled': self.two_factor_enabled,
            'email_notifications': self.email_notifications,
            'push_notifications': self.push_notifications,
            'appointment_reminders': self.appointment_reminders,
            'language': self.language,
            'date_format': self.date_format,
            'timezone': self.timezone,
            'session_timeout': self.session_timeout,
            **self.additional_settings
        }
