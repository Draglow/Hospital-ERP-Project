from django.db import models
from django.utils import timezone
from decimal import Decimal
from appointments.models import Appointment

class Medicine(models.Model):
    """Medicine/Drug inventory model"""

    CATEGORY_CHOICES = [
        ('antibiotic', 'Antibiotic'),
        ('painkiller', 'Painkiller'),
        ('vitamin', 'Vitamin/Supplement'),
        ('cardiac', 'Cardiac Medication'),
        ('diabetes', 'Diabetes Medication'),
        ('respiratory', 'Respiratory Medication'),
        ('gastrointestinal', 'Gastrointestinal'),
        ('neurological', 'Neurological'),
        ('dermatological', 'Dermatological'),
        ('ophthalmological', 'Eye Medication'),
        ('contraceptive', 'Contraceptive'),
        ('vaccine', 'Vaccine'),
        ('other', 'Other'),
    ]

    FORM_CHOICES = [
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('cream', 'Cream/Ointment'),
        ('drops', 'Drops'),
        ('inhaler', 'Inhaler'),
        ('suppository', 'Suppository'),
        ('patch', 'Patch'),
        ('other', 'Other'),
    ]

    # Basic Information
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    brand_name = models.CharField(max_length=200, blank=True)
    manufacturer = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    form = models.CharField(max_length=20, choices=FORM_CHOICES)
    strength = models.CharField(max_length=50, help_text="e.g., 500mg, 10ml")

    # Inventory Information
    stock_quantity = models.PositiveIntegerField(default=0)
    minimum_stock_level = models.PositiveIntegerField(default=10)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Purchase cost")

    # Dates
    manufacture_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField()

    # Additional Information
    description = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)
    contraindications = models.TextField(blank=True)
    storage_instructions = models.TextField(blank=True)

    # System Fields
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.strength}) - {self.stock_quantity} units"

    def is_low_stock(self):
        """Check if medicine is below minimum stock level"""
        try:
            return self.stock_quantity <= self.minimum_stock_level
        except (TypeError, ValueError):
            return False

    def is_expired(self):
        """Check if medicine is expired"""
        try:
            if not self.expiry_date:
                return False
            return timezone.now().date() > self.expiry_date
        except (TypeError, ValueError, AttributeError):
            return False

    def is_expiring_soon(self, days=30):
        """Check if medicine is expiring within specified days"""
        try:
            from datetime import timedelta
            if not self.expiry_date:
                return False
            warning_date = timezone.now().date() + timedelta(days=days)
            return self.expiry_date <= warning_date
        except (TypeError, ValueError, AttributeError):
            return False

    def can_dispense(self, quantity):
        """Check if specified quantity can be dispensed"""
        try:
            return (
                self.is_active and
                self.stock_quantity >= quantity and
                not self.is_expiring_soon(7)  # Don't dispense if expiring in 7 days
            )
        except (TypeError, ValueError):
            return False

    class Meta:
        ordering = ['name']
        verbose_name = 'Medicine'
        verbose_name_plural = 'Medicines'


class Prescription(models.Model):
    """Prescription model linking appointments to medicines"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('dispensed', 'Dispensed'),
        ('partially_dispensed', 'Partially Dispensed'),
        ('cancelled', 'Cancelled'),
    ]

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescriptions')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='prescriptions')

    # Prescription Details
    dosage = models.CharField(max_length=100, help_text="e.g., 1 tablet twice daily")
    quantity_prescribed = models.PositiveIntegerField()
    quantity_dispensed = models.PositiveIntegerField(default=0)
    duration_days = models.PositiveIntegerField(help_text="Treatment duration in days")

    # Instructions
    instructions = models.TextField(help_text="Special instructions for patient")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # System Fields
    prescribed_date = models.DateTimeField(auto_now_add=True)
    dispensed_date = models.DateTimeField(null=True, blank=True)
    dispensed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dispensed_prescriptions'
    )

    def __str__(self):
        return f"{self.medicine.name} for {self.appointment.patient.get_full_name()}"

    def is_fully_dispensed(self):
        """Check if prescription is fully dispensed"""
        return self.quantity_dispensed >= self.quantity_prescribed

    def remaining_quantity(self):
        """Get remaining quantity to dispense"""
        return max(0, self.quantity_prescribed - self.quantity_dispensed)

    class Meta:
        ordering = ['-prescribed_date']
        verbose_name = 'Prescription'
        verbose_name_plural = 'Prescriptions'
