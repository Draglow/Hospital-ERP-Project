from django.db import models
from django.utils import timezone
from decimal import Decimal
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment

class Invoice(models.Model):
    """Invoice model for billing patients"""

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
        ('insurance', 'Insurance'),
        ('credit', 'Credit'),
    ]

    # Core Fields
    invoice_number = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='invoices')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='invoices', null=True, blank=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')

    # Invoice Details
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    # Financial Information
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    # Payment Information
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)

    # Additional Information
    notes = models.TextField(blank=True)

    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate invoice number: INV + year + month + sequential number
            now = timezone.now()
            year_month = now.strftime('%Y%m')
            last_invoice = Invoice.objects.filter(
                invoice_number__startswith=f'INV{year_month}'
            ).order_by('invoice_number').last()

            if last_invoice:
                last_number = int(last_invoice.invoice_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1

            self.invoice_number = f'INV{year_month}{new_number:04d}'

        # Calculate total amount
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number} - {self.patient.get_full_name()} - {self.total_amount} ETB"

    def get_balance(self):
        """Get remaining balance"""
        return self.total_amount - self.paid_amount

    @property
    def balance_due(self):
        """Property for remaining balance - used in templates"""
        return self.total_amount - self.paid_amount

    def is_fully_paid(self):
        """Check if invoice is fully paid"""
        return self.paid_amount >= self.total_amount

    def is_overdue(self):
        """Check if invoice is overdue"""
        return timezone.now().date() > self.due_date and not self.is_fully_paid()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'


class InvoiceItem(models.Model):
    """Individual items in an invoice"""

    ITEM_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('procedure', 'Medical Procedure'),
        ('medication', 'Medication'),
        ('lab_test', 'Laboratory Test'),
        ('imaging', 'Medical Imaging'),
        ('room_charge', 'Room Charge'),
        ('other', 'Other'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    description = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

        # Update invoice subtotal
        self.invoice.subtotal = sum(item.total_price for item in self.invoice.items.all())
        self.invoice.save()

    def __str__(self):
        return f"{self.description} - {self.quantity} x {self.unit_price} ETB"

    class Meta:
        verbose_name = 'Invoice Item'
        verbose_name_plural = 'Invoice Items'
