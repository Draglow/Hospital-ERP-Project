from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Notification, NotificationPreference
from appointments.models import Appointment
from patients.models import Patient
from billing.models import Invoice
from pharmacy.models import Medicine

User = get_user_model()


@receiver(post_save, sender=User)
def create_notification_preferences(sender, instance, created, **kwargs):
    """Create notification preferences for new users"""
    if created:
        NotificationPreference.objects.create(user=instance)


@receiver(post_save, sender=Appointment)
def appointment_notifications(sender, instance, created, **kwargs):
    """Create notifications for appointment events"""
    if created:
        # Notify doctor about new appointment
        Notification.objects.create(
            title="New Appointment Scheduled",
            message=f"New appointment with {instance.patient.get_full_name()} on {instance.appointment_date} at {instance.appointment_time}",
            notification_type='appointment',
            priority='normal',
            recipient=instance.doctor.user,
            sender=instance.created_by,
            action_url=f"/appointments/{instance.pk}/"
        )
        
        # Notify admin users about new appointment
        admin_users = User.objects.filter(role='admin')
        for admin in admin_users:
            Notification.objects.create(
                title="New Appointment Created",
                message=f"Appointment scheduled for {instance.patient.get_full_name()} with Dr. {instance.doctor.get_full_name()}",
                notification_type='appointment',
                priority='low',
                recipient=admin,
                sender=instance.created_by,
                action_url=f"/appointments/{instance.pk}/"
            )


@receiver(pre_save, sender=Appointment)
def appointment_status_change_notifications(sender, instance, **kwargs):
    """Notify about appointment status changes"""
    if instance.pk:  # Only for existing appointments
        try:
            old_instance = Appointment.objects.get(pk=instance.pk)
            if old_instance.status != instance.status:
                # Status changed
                if instance.status == 'cancelled':
                    # Notify doctor about cancellation
                    Notification.objects.create(
                        title="Appointment Cancelled",
                        message=f"Appointment with {instance.patient.get_full_name()} on {instance.appointment_date} has been cancelled",
                        notification_type='appointment',
                        priority='high',
                        recipient=instance.doctor.user,
                        action_url=f"/appointments/{instance.pk}/"
                    )
                elif instance.status == 'completed':
                    # Notify about completion
                    Notification.objects.create(
                        title="Appointment Completed",
                        message=f"Appointment with {instance.patient.get_full_name()} has been completed",
                        notification_type='appointment',
                        priority='normal',
                        recipient=instance.doctor.user,
                        action_url=f"/appointments/{instance.pk}/"
                    )
        except Appointment.DoesNotExist:
            pass


@receiver(post_save, sender=Patient)
def patient_registration_notification(sender, instance, created, **kwargs):
    """Notify about new patient registrations"""
    if created:
        # Notify all doctors and admin users
        users_to_notify = User.objects.filter(role__in=['doctor', 'admin', 'nurse'])
        for user in users_to_notify:
            Notification.objects.create(
                title="New Patient Registered",
                message=f"New patient {instance.get_full_name()} has been registered",
                notification_type='patient',
                priority='normal',
                recipient=user,
                action_url=f"/patients/{instance.pk}/"
            )


@receiver(post_save, sender=Invoice)
def billing_notifications(sender, instance, created, **kwargs):
    """Create notifications for billing events"""
    if created:
        # Notify admin and billing staff about new invoice
        users_to_notify = User.objects.filter(role__in=['admin', 'receptionist'])
        for user in users_to_notify:
            Notification.objects.create(
                title="New Invoice Created",
                message=f"Invoice {instance.invoice_number} created for {instance.patient.get_full_name()} - {instance.total_amount} ETB",
                notification_type='billing',
                priority='normal',
                recipient=user,
                action_url=f"/billing/{instance.pk}/"
            )


@receiver(pre_save, sender=Invoice)
def invoice_payment_notifications(sender, instance, **kwargs):
    """Notify about invoice payment status changes"""
    if instance.pk:  # Only for existing invoices
        try:
            old_instance = Invoice.objects.get(pk=instance.pk)
            if old_instance.status != instance.status:
                if instance.status == 'paid':
                    # Invoice fully paid
                    users_to_notify = User.objects.filter(role__in=['admin', 'receptionist'])
                    for user in users_to_notify:
                        Notification.objects.create(
                            title="Invoice Paid",
                            message=f"Invoice {instance.invoice_number} has been fully paid - {instance.total_amount} ETB",
                            notification_type='billing',
                            priority='normal',
                            recipient=user,
                            action_url=f"/billing/{instance.pk}/"
                        )
                elif instance.status == 'overdue':
                    # Invoice overdue
                    users_to_notify = User.objects.filter(role__in=['admin', 'receptionist'])
                    for user in users_to_notify:
                        Notification.objects.create(
                            title="Invoice Overdue",
                            message=f"Invoice {instance.invoice_number} is overdue - {instance.balance_due} ETB remaining",
                            notification_type='billing',
                            priority='high',
                            recipient=user,
                            action_url=f"/billing/{instance.pk}/"
                        )
        except Invoice.DoesNotExist:
            pass


def check_low_stock_medicines():
    """Check for low stock medicines and create notifications"""
    from django.db import models
    low_stock_medicines = Medicine.objects.filter(
        stock_quantity__lte=models.F('minimum_stock_level'),
        is_active=True
    )
    
    if low_stock_medicines.exists():
        # Notify pharmacists and admin
        users_to_notify = User.objects.filter(role__in=['pharmacist', 'admin'])
        for user in users_to_notify:
            for medicine in low_stock_medicines:
                # Check if notification already exists for this medicine
                existing_notification = Notification.objects.filter(
                    recipient=user,
                    notification_type='pharmacy',
                    title__contains=f"Low Stock: {medicine.name}",
                    is_read=False
                ).exists()
                
                if not existing_notification:
                    Notification.objects.create(
                        title=f"Low Stock: {medicine.name}",
                        message=f"{medicine.name} is running low. Current stock: {medicine.stock_quantity} units (Minimum: {medicine.minimum_stock_level})",
                        notification_type='pharmacy',
                        priority='high',
                        recipient=user,
                        action_url=f"/pharmacy/{medicine.pk}/"
                    )


def check_expiring_medicines():
    """Check for medicines expiring soon and create notifications"""
    from datetime import timedelta
    from django.utils import timezone
    
    expiring_medicines = Medicine.objects.filter(
        expiry_date__lte=timezone.now().date() + timedelta(days=30),
        expiry_date__gt=timezone.now().date(),
        is_active=True
    )
    
    if expiring_medicines.exists():
        # Notify pharmacists and admin
        users_to_notify = User.objects.filter(role__in=['pharmacist', 'admin'])
        for user in users_to_notify:
            for medicine in expiring_medicines:
                # Check if notification already exists for this medicine
                existing_notification = Notification.objects.filter(
                    recipient=user,
                    notification_type='pharmacy',
                    title__contains=f"Expiring Soon: {medicine.name}",
                    is_read=False
                ).exists()
                
                if not existing_notification:
                    days_to_expiry = (medicine.expiry_date - timezone.now().date()).days
                    Notification.objects.create(
                        title=f"Expiring Soon: {medicine.name}",
                        message=f"{medicine.name} expires in {days_to_expiry} days on {medicine.expiry_date}",
                        notification_type='pharmacy',
                        priority='high' if days_to_expiry <= 7 else 'normal',
                        recipient=user,
                        action_url=f"/pharmacy/{medicine.pk}/"
                    )
