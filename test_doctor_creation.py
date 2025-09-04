#!/usr/bin/env python
"""
Test script to verify doctor creation works correctly
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_erp.settings')
django.setup()

from doctors.models import Doctor
from accounts.models import User

def test_doctor_creation():
    """Test creating a doctor with all required fields"""
    try:
        # Test data
        user_data = {
            'username': 'dr.test.doctor',
            'email': 'test.doctor@example.com',
            'first_name': 'Test',
            'last_name': 'Doctor',
            'role': 'doctor',
            'phone': '+251911234567',
            'is_staff': True
        }
        
        doctor_data = {
            'license_number': 'ETH-MD-2024-TEST',
            'specialty': 'general',
            'sub_specialty': 'Family Medicine',
            'years_of_experience': 5,
            'medical_school': 'Addis Ababa University',
            'graduation_year': 2019,
            'certifications': 'MD, General Practice Certificate',
            'consultation_fee': 500.00,
            'availability_status': 'full_time',
            'bio': 'Test doctor for mobile functionality testing',
            'languages_spoken': 'Amharic, English',
        }
        
        # Create user first
        user = User.objects.create_user(**user_data)
        user.set_password('testpassword123')
        user.save()
        print(f"✅ User created successfully: {user.username}")
        
        # Create doctor profile
        doctor = Doctor.objects.create(user=user, **doctor_data)
        print(f"✅ Doctor created successfully: {doctor.get_full_name()}")
        
        # Verify all required fields
        print(f"   - Medical School: {doctor.medical_school}")
        print(f"   - Graduation Year: {doctor.graduation_year}")
        print(f"   - License Number: {doctor.license_number}")
        print(f"   - Specialty: {doctor.get_specialty_display()}")
        
        # Clean up - delete the test doctor and user
        doctor.delete()
        user.delete()
        print("✅ Test doctor and user deleted successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating doctor: {str(e)}")
        # Clean up in case of error
        try:
            if 'user' in locals():
                user.delete()
        except:
            pass
        return False

def test_required_fields():
    """Test that required fields are properly validated"""
    print("\n🧪 Testing required field validation...")
    
    try:
        # Try to create doctor without medical_school (should fail)
        user = User.objects.create_user(
            username='dr.test.incomplete',
            email='incomplete@example.com',
            first_name='Incomplete',
            last_name='Doctor',
            role='doctor'
        )
        
        # This should fail due to missing medical_school
        doctor = Doctor.objects.create(
            user=user,
            license_number='ETH-MD-2024-INCOMPLETE',
            specialty='general',
            # medical_school is missing - should cause error
            graduation_year=2020,
        )
        
        # If we get here, something is wrong
        print("❌ Doctor creation should have failed due to missing medical_school")
        doctor.delete()
        user.delete()
        return False
        
    except Exception as e:
        print(f"✅ Correctly caught missing field error: {str(e)}")
        # Clean up
        try:
            if 'user' in locals():
                user.delete()
        except:
            pass
        return True

if __name__ == '__main__':
    print("🏥 Testing Mobile Doctor Creation Functionality...")
    print("=" * 60)
    
    # Test complete doctor creation
    success1 = test_doctor_creation()
    
    # Test required field validation
    success2 = test_required_fields()
    
    # Summary
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 All tests passed! Doctor creation should work correctly.")
        print("\n📱 You can now test in the mobile interface:")
        print("   1. Go to: http://localhost:8000/doctors/add/?mobile=1")
        print("   2. Fill out all required fields including:")
        print("      - Medical School (required)")
        print("      - Graduation Year (required)")
        print("      - License Number (required)")
        print("   3. Submit the form")
        print("   4. Verify the doctor is created successfully")
    else:
        print("💥 Some tests failed. Check the errors above.")
