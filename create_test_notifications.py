#!/usr/bin/env python3
"""
Simple script to create test notifications for debugging delete functionality.
Run this in Django shell or as a management command.
"""

from django.contrib.auth.models import User
from notifications.models import Notification

def create_test_notifications():
    """Create test notifications for the current user"""
    
    # Get the first user (or create one if none exists)
    try:
        user = User.objects.first()
        if not user:
            print("No users found. Creating a test user...")
            user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123'
            )
            print(f"Created test user: {user.username}")
    except Exception as e:
        print(f"Error getting/creating user: {e}")
        return

    # Create test notifications
    test_notifications = [
        {
            'title': 'New Patient Registration',
            'message': 'John Doe has been registered as a new patient',
            'notification_type': 'patient',
            'priority': 'normal',
        },
        {
            'title': 'Appointment Scheduled',
            'message': 'Dr. Smith has a new appointment at 3:00 PM',
            'notification_type': 'appointment',
            'priority': 'high',
        },
        {
            'title': 'Medicine Stock Alert',
            'message': 'Paracetamol stock is running low (5 units remaining)',
            'notification_type': 'pharmacy',
            'priority': 'high',
        },
        {
            'title': 'Billing Invoice Generated',
            'message': 'Invoice #INV-2024-001 has been generated for Patient ID: 12345',
            'notification_type': 'billing',
            'priority': 'normal',
        },
        {
            'title': 'System Maintenance',
            'message': 'Scheduled maintenance will occur tonight at 2:00 AM',
            'notification_type': 'system',
            'priority': 'low',
        }
    ]

    created_count = 0
    for notification_data in test_notifications:
        try:
            # Check if notification already exists
            existing = Notification.objects.filter(
                recipient=user,
                title=notification_data['title']
            ).first()
            
            if not existing:
                notification = Notification.objects.create(
                    recipient=user,
                    **notification_data
                )
                print(f"Created notification: {notification.title}")
                created_count += 1
            else:
                print(f"Notification already exists: {notification_data['title']}")
                
        except Exception as e:
            print(f"Error creating notification '{notification_data['title']}': {e}")

    print(f"\nSummary: Created {created_count} new notifications")
    print(f"Total notifications for {user.username}: {Notification.objects.filter(recipient=user).count()}")

if __name__ == "__main__":
    print("Creating test notifications...")
    create_test_notifications()
    print("Done!")

# Django shell usage:
# python manage.py shell
# exec(open('create_test_notifications.py').read())

# Or run directly if Django is set up:
# python create_test_notifications.py
