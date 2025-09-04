#!/usr/bin/env python3
"""
Django management command to debug notification issues.
Run this to check if notifications exist and create test data if needed.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_erp.settings')
django.setup()

from django.contrib.auth.models import User
from notifications.models import Notification

def debug_notifications():
    print("=== NOTIFICATION DEBUG SCRIPT ===\n")
    
    # Check users
    users = User.objects.all()
    print(f"Total users in system: {users.count()}")
    
    if users.count() == 0:
        print("❌ No users found! Creating a test user...")
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        print(f"✅ Created user: {user.username}")
    else:
        user = users.first()
        print(f"✅ Using existing user: {user.username}")
    
    # Check notifications
    notifications = Notification.objects.filter(recipient=user)
    print(f"\nNotifications for {user.username}: {notifications.count()}")
    
    if notifications.count() == 0:
        print("❌ No notifications found! Creating test notifications...")
        
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
            }
        ]
        
        for notification_data in test_notifications:
            notification = Notification.objects.create(
                recipient=user,
                **notification_data
            )
            print(f"✅ Created: {notification.title}")
        
        print(f"\n✅ Created {len(test_notifications)} test notifications")
    else:
        print("✅ Notifications exist:")
        for notification in notifications[:5]:  # Show first 5
            status = "UNREAD" if not notification.is_read else "READ"
            print(f"  - [{status}] {notification.title} (ID: {notification.pk})")
    
    # Check notification URLs
    print(f"\n=== URL TESTING ===")
    print("Test these URLs in your browser:")
    print("1. Main notifications: http://localhost:8000/notifications/")
    print("2. Debug notifications: http://localhost:8000/notifications/debug/")
    print("3. Dropdown: http://localhost:8000/notifications/dropdown/")
    
    # Check delete endpoint
    if notifications.exists():
        first_notification = notifications.first()
        print(f"4. Test delete: http://localhost:8000/notifications/delete/{first_notification.pk}/")
        print(f"   (POST request with CSRF token)")
    
    print(f"\n=== SUMMARY ===")
    print(f"✅ Users: {users.count()}")
    print(f"✅ Notifications: {notifications.count()}")
    print(f"✅ Test user: {user.username}")
    
    if notifications.count() > 0:
        print("\n🎉 Everything looks good! Try accessing the notifications page now.")
        print("   If delete buttons still don't work, check browser console for JavaScript errors.")
    else:
        print("\n❌ Still no notifications. Check your Django models and database.")

if __name__ == "__main__":
    debug_notifications()
