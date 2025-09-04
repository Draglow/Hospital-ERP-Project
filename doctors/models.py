from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

class Doctor(models.Model):
    """Doctor model linked to User with medical specialization"""

    SPECIALTY_CHOICES = [
        ('general', 'General Medicine'),
        ('pediatrics', 'Pediatrics'),
        ('surgery', 'Surgery'),
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('gynecology', 'Gynecology'),
        ('dermatology', 'Dermatology'),
        ('psychiatry', 'Psychiatry'),
        ('radiology', 'Radiology'),
        ('anesthesiology', 'Anesthesiology'),
        ('emergency', 'Emergency Medicine'),
        ('internal', 'Internal Medicine'),
        ('ophthalmology', 'Ophthalmology'),
        ('ent', 'ENT (Ear, Nose, Throat)'),
    ]

    AVAILABILITY_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('on_call', 'On Call'),
        ('consultant', 'Consultant'),
    ]

    # Link to User model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Professional Information
    license_number = models.CharField(max_length=50, unique=True)
    specialty = models.CharField(max_length=20, choices=SPECIALTY_CHOICES)
    sub_specialty = models.CharField(max_length=100, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)

    # Medical Education
    medical_school = models.CharField(max_length=200)
    graduation_year = models.PositiveIntegerField()
    certifications = models.TextField(blank=True, help_text="Additional certifications and qualifications")

    # Practice Information
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, help_text="Fee in ETB")
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='full_time')

    # Schedule (simplified - can be expanded later)
    monday_start = models.TimeField(blank=True, null=True)
    monday_end = models.TimeField(blank=True, null=True)
    tuesday_start = models.TimeField(blank=True, null=True)
    tuesday_end = models.TimeField(blank=True, null=True)
    wednesday_start = models.TimeField(blank=True, null=True)
    wednesday_end = models.TimeField(blank=True, null=True)
    thursday_start = models.TimeField(blank=True, null=True)
    thursday_end = models.TimeField(blank=True, null=True)
    friday_start = models.TimeField(blank=True, null=True)
    friday_end = models.TimeField(blank=True, null=True)
    saturday_start = models.TimeField(blank=True, null=True)
    saturday_end = models.TimeField(blank=True, null=True)
    sunday_start = models.TimeField(blank=True, null=True)
    sunday_end = models.TimeField(blank=True, null=True)

    # Additional Information
    bio = models.TextField(blank=True, help_text="Doctor's biography for public display")
    languages_spoken = models.CharField(max_length=200, default="Amharic, English")

    # System Fields
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.get_specialty_display()}"

    def get_full_name(self):
        return f"Dr. {self.user.get_full_name()}"

    def is_available_today(self):
        """Check if doctor is available today (simplified logic)"""
        from datetime import datetime
        today = datetime.now().strftime('%A').lower()
        start_time = getattr(self, f'{today}_start')
        end_time = getattr(self, f'{today}_end')
        return start_time and end_time

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
