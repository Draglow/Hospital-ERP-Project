from django.db import models
from django.utils import timezone
from patients.models import Patient
from doctors.models import Doctor

class Appointment(models.Model):
    """Appointment model for scheduling patient visits"""

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
        ('rescheduled', 'Rescheduled'),
    ]

    APPOINTMENT_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('emergency', 'Emergency'),
        ('surgery', 'Surgery'),
        ('checkup', 'Regular Checkup'),
        ('vaccination', 'Vaccination'),
        ('lab_test', 'Lab Test'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    # Core Fields
    appointment_id = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')

    # Scheduling
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(default=30)

    # Appointment Details
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, default='consultation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')

    # Medical Information
    chief_complaint = models.TextField(help_text="Patient's main concern or reason for visit")
    symptoms = models.TextField(blank=True, help_text="Detailed symptoms")
    notes = models.TextField(blank=True, help_text="Additional notes")

    # Consultation Details (filled during/after appointment)
    diagnosis = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(blank=True, null=True)

    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_appointments'
    )

    def save(self, *args, **kwargs):
        if not self.appointment_id:
            # Generate appointment ID: APT + year + month + sequential number
            now = timezone.now()
            year_month = now.strftime('%Y%m')
            last_appointment = Appointment.objects.filter(
                appointment_id__startswith=f'APT{year_month}'
            ).order_by('appointment_id').last()

            if last_appointment:
                last_number = int(last_appointment.appointment_id[-4:])
                new_number = last_number + 1
            else:
                new_number = 1

            self.appointment_id = f'APT{year_month}{new_number:04d}'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.appointment_id} - {self.patient.get_full_name()} with {self.doctor.get_full_name()}"

    def get_appointment_datetime(self):
        """Combine date and time for easier handling"""
        from datetime import datetime
        # Create timezone-aware datetime
        naive_datetime = datetime.combine(self.appointment_date, self.appointment_time)
        return timezone.make_aware(naive_datetime)

    def is_past_due(self):
        """Check if appointment is past due"""
        return self.get_appointment_datetime() < timezone.now()

    def can_be_cancelled(self):
        """Check if appointment can be cancelled"""
        try:
            # Can't cancel if already cancelled or completed
            if self.status in ['cancelled', 'completed']:
                return False

            # Can't cancel if appointment is in the past
            appointment_datetime = self.get_appointment_datetime()
            now = timezone.now()

            # Allow cancellation up to 1 hour before appointment (more lenient than 2 hours)
            from datetime import timedelta
            cancellation_deadline = appointment_datetime - timedelta(hours=1)

            return now < cancellation_deadline
        except Exception:
            # If there's any error, default to not allowing cancellation
            return False

    class Meta:
        ordering = ['appointment_date', 'appointment_time']
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        unique_together = ['doctor', 'appointment_date', 'appointment_time']
