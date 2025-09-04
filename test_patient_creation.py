#!/usr/bin/env python
"""
Test script to verify patient creation works correctly
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_erp.settings')
django.setup()

from patients.models import Patient

def test_patient_creation():
    """Test creating a patient with all required fields"""
    try:
        # Test data
        patient_data = {
            'first_name': 'Test',
            'last_name': 'Patient',
            'date_of_birth': '1990-01-01',
            'gender': 'M',
            'blood_type': 'O+',
            'kebele': 'Test Kebele',
            'woreda': 'Test Woreda',
            'city': 'Addis Ababa',
            'region': 'Addis Ababa',
            'phone': '+251911234567',
            'email': 'test@example.com',
            'emergency_contact_name': 'Test Emergency Contact',
            'emergency_contact_phone': '+251911234568',
            'emergency_contact_relationship': 'parent',
            'medical_history': 'No significant medical history',
            'allergies': 'No known allergies',
            'current_medications': 'None',
        }
        
        # Create patient
        patient = Patient.objects.create(**patient_data)
        print(f"✅ Patient created successfully: {patient.get_full_name()} (ID: {patient.patient_id})")
        
        # Verify all fields
        print(f"   - Kebele: {patient.kebele}")
        print(f"   - Woreda: {patient.woreda}")
        print(f"   - Emergency Contact: {patient.emergency_contact_name}")
        
        # Clean up - delete the test patient
        patient.delete()
        print("✅ Test patient deleted successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating patient: {str(e)}")
        return False

if __name__ == '__main__':
    print("Testing patient creation...")
    success = test_patient_creation()
    if success:
        print("\n🎉 All tests passed! Patient creation should work correctly.")
    else:
        print("\n💥 Tests failed! There may still be issues with patient creation.")
