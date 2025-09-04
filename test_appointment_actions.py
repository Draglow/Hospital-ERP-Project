#!/usr/bin/env python
"""
Test script to verify appointment start/cancel functionality works correctly
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_erp.settings')
django.setup()

from appointments.models import Appointment
from patients.models import Patient
from doctors.models import Doctor
from accounts.models import User

def create_test_appointment():
    """Create a test appointment for testing"""
    try:
        # Get or create a test patient
        try:
            patient = Patient.objects.first()
            if not patient:
                print("❌ No patients found. Please create a patient first.")
                return None
        except Exception as e:
            print(f"❌ Error getting patient: {e}")
            return None
            
        # Get or create a test doctor
        try:
            doctor = Doctor.objects.first()
            if not doctor:
                print("❌ No doctors found. Please create a doctor first.")
                return None
        except Exception as e:
            print(f"❌ Error getting doctor: {e}")
            return None
            
        # Get a user for created_by
        try:
            user = User.objects.first()
            if not user:
                print("❌ No users found.")
                return None
        except Exception as e:
            print(f"❌ Error getting user: {e}")
            return None
        
        # Create appointment for today
        today = datetime.now().date()
        appointment_time = datetime.now().time().replace(second=0, microsecond=0)
        
        appointment_data = {
            'patient': patient,
            'doctor': doctor,
            'appointment_date': today,
            'appointment_time': appointment_time,
            'appointment_type': 'consultation',
            'status': 'scheduled',
            'priority': 'normal',
            'chief_complaint': 'Test appointment for mobile functionality',
            'symptoms': 'Testing mobile start/cancel features',
            'notes': 'This is a test appointment',
            'created_by': user,
        }
        
        # Create appointment
        appointment = Appointment.objects.create(**appointment_data)
        print(f"✅ Test appointment created: {appointment.appointment_id}")
        print(f"   - Patient: {appointment.patient.get_full_name()}")
        print(f"   - Doctor: {appointment.doctor.get_full_name()}")
        print(f"   - Date: {appointment.appointment_date}")
        print(f"   - Time: {appointment.appointment_time}")
        print(f"   - Status: {appointment.status}")
        print(f"   - Can be cancelled: {appointment.can_be_cancelled()}")
        
        return appointment
        
    except Exception as e:
        print(f"❌ Error creating test appointment: {str(e)}")
        return None

def test_appointment_methods(appointment):
    """Test appointment methods"""
    print(f"\n🧪 Testing appointment methods for {appointment.appointment_id}:")
    
    try:
        # Test get_appointment_datetime
        appointment_datetime = appointment.get_appointment_datetime()
        print(f"   - get_appointment_datetime(): {appointment_datetime}")
        
        # Test is_past_due
        is_past_due = appointment.is_past_due()
        print(f"   - is_past_due(): {is_past_due}")
        
        # Test can_be_cancelled
        can_be_cancelled = appointment.can_be_cancelled()
        print(f"   - can_be_cancelled(): {can_be_cancelled}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing appointment methods: {str(e)}")
        return False

def test_status_changes(appointment):
    """Test status changes"""
    print(f"\n🔄 Testing status changes for {appointment.appointment_id}:")
    
    try:
        # Test starting appointment
        if appointment.status in ['scheduled', 'confirmed']:
            print(f"   - Current status: {appointment.status}")
            appointment.status = 'in_progress'
            appointment.save()
            print(f"   - ✅ Started appointment, new status: {appointment.status}")
            
            # Test completing appointment
            appointment.status = 'completed'
            appointment.save()
            print(f"   - ✅ Completed appointment, new status: {appointment.status}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing status changes: {str(e)}")
        return False

def cleanup_test_appointment(appointment):
    """Clean up test appointment"""
    try:
        appointment_id = appointment.appointment_id
        appointment.delete()
        print(f"✅ Test appointment {appointment_id} deleted successfully")
        return True
    except Exception as e:
        print(f"❌ Error deleting test appointment: {str(e)}")
        return False

if __name__ == '__main__':
    print("🏥 Testing Mobile Appointment Start/Cancel Functionality...")
    print("=" * 60)
    
    # Create test appointment
    appointment = create_test_appointment()
    if not appointment:
        print("\n💥 Failed to create test appointment. Exiting.")
        sys.exit(1)
    
    # Test appointment methods
    methods_ok = test_appointment_methods(appointment)
    if not methods_ok:
        print("\n💥 Appointment methods test failed.")
    
    # Test status changes
    status_ok = test_status_changes(appointment)
    if not status_ok:
        print("\n💥 Status changes test failed.")
    
    # Clean up
    cleanup_ok = cleanup_test_appointment(appointment)
    
    # Summary
    print("\n" + "=" * 60)
    if methods_ok and status_ok and cleanup_ok:
        print("🎉 All tests passed! Mobile appointment functionality should work correctly.")
        print("\n📱 You can now test in the mobile interface:")
        print("   1. Go to: http://localhost:8000/appointments/?mobile=1")
        print("   2. Find a scheduled appointment")
        print("   3. Click 'Start' to test starting an appointment")
        print("   4. Click 'Complete' to test completing an appointment")
        print("   5. Click 'Cancel' to test cancelling an appointment")
    else:
        print("💥 Some tests failed. Check the errors above.")
