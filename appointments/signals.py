# Appointments signals
# Note: All appointment-related signals are actually implemented in notifications/signals.py
# This file exists to prevent import errors if something tries to import apps.appointments.signals

# Import the actual signals from notifications to ensure they're registered
from notifications.signals import (
    appointment_notifications,
    appointment_status_change_notifications
)

# Re-export the signals for compatibility
__all__ = [
    'appointment_notifications',
    'appointment_status_change_notifications'
]
