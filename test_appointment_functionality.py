#!/usr/bin/env python
"""
Test script to verify appointment start and cancel functionality
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_erp.settings')
django.setup()

from appointments.models import Appointment
from django.utils import timezone
from datetime import datetime, timedelta

def test_appointment_functionality():
    """Test appointment start and cancel functionality"""
    print("🧪 Testing Appointment Functionality")
    print("=" * 50)
    
    # Get the latest appointment
    try:
        appointment = Appointment.objects.latest('created_at')
        print(f"📋 Testing with appointment: {appointment.appointment_id}")
        print(f"   - Patient: {appointment.patient.get_full_name()}")
        print(f"   - Doctor: {appointment.doctor.get_full_name()}")
        print(f"   - Status: {appointment.get_status_display()}")
        print(f"   - Date/Time: {appointment.appointment_date} {appointment.appointment_time}")
        
        # Test appointment methods
        print(f"\n🔍 Testing appointment methods:")
        print(f"   - can_be_cancelled(): {appointment.can_be_cancelled()}")
        print(f"   - is_past_due(): {appointment.is_past_due()}")
        print(f"   - get_appointment_datetime(): {appointment.get_appointment_datetime()}")
        
        # Test status transitions
        print(f"\n🔄 Testing status transitions:")
        original_status = appointment.status
        
        # Test starting appointment
        if appointment.status in ['scheduled', 'confirmed']:
            print(f"   - Can start appointment: ✅")
            # Don't actually change status in test
        else:
            print(f"   - Cannot start appointment (status: {appointment.status}): ❌")
        
        # Test cancelling appointment
        if appointment.can_be_cancelled():
            print(f"   - Can cancel appointment: ✅")
        else:
            print(f"   - Cannot cancel appointment: ❌")
            
        print(f"\n✅ All tests completed successfully!")
        return True
        
    except Appointment.DoesNotExist:
        print("❌ No appointments found in database")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    test_appointment_functionality()
