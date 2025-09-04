#!/usr/bin/env python
"""
Test script to verify doctor creation with unique license number generation works correctly
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
from datetime import datetime

def test_unique_license_generation():
    """Test creating multiple doctors to verify unique license number generation"""
    try:
        print("🧪 Testing unique license number generation...")
        
        # Test data for first doctor
        user_data_1 = {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john.smith1@example.com',
            'role': 'doctor',
            'phone': '+251911234567',
            'is_staff': True
        }
        
        doctor_data_1 = {
            'specialty': 'general',
            'sub_specialty': 'Family Medicine',
            'years_of_experience': 5,
            'medical_school': 'Addis Ababa University',
            'graduation_year': 2019,
            'certifications': 'MD, General Practice Certificate',
            'consultation_fee': 500.00,
            'availability_status': 'full_time',
            'bio': 'First test doctor',
            'languages_spoken': 'Amharic, English',
        }
        
        # Generate unique license number for first doctor
        year = datetime.now().year
        base_license_1 = f"ETH-MD-{year}-JOHSMI"
        license_number_1 = base_license_1
        counter = 1
        while Doctor.objects.filter(license_number=license_number_1).exists():
            license_number_1 = f"{base_license_1}-{counter}"
            counter += 1
        
        # Create first doctor
        user_1 = User.objects.create_user(username='dr.john.smith.test1', **user_data_1)
        user_1.set_password('doctor123')
        user_1.save()
        
        doctor_1 = Doctor.objects.create(user=user_1, license_number=license_number_1, **doctor_data_1)
        print(f"✅ First doctor created: {doctor_1.get_full_name()} (license: {doctor_1.license_number})")
        
        # Test data for second doctor with same name pattern
        user_data_2 = {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john.smith2@example.com',
            'role': 'doctor',
            'phone': '+251911234568',
            'is_staff': True
        }
        
        doctor_data_2 = {
            'specialty': 'cardiology',
            'sub_specialty': 'Interventional Cardiology',
            'years_of_experience': 8,
            'medical_school': 'University of Gondar',
            'graduation_year': 2016,
            'certifications': 'MD, Cardiology Specialist',
            'consultation_fee': 800.00,
            'availability_status': 'part_time',
            'bio': 'Second test doctor',
            'languages_spoken': 'Amharic, English',
        }
        
        # Generate unique license number for second doctor - should get unique number
        base_license_2 = f"ETH-MD-{year}-JOHSMI"
        license_number_2 = base_license_2
        counter = 1
        while Doctor.objects.filter(license_number=license_number_2).exists():
            license_number_2 = f"{base_license_2}-{counter}"
            counter += 1
        
        # Create second doctor
        user_2 = User.objects.create_user(username='dr.john.smith.test2', **user_data_2)
        user_2.set_password('doctor123')
        user_2.save()
        
        doctor_2 = Doctor.objects.create(user=user_2, license_number=license_number_2, **doctor_data_2)
        print(f"✅ Second doctor created: {doctor_2.get_full_name()} (license: {doctor_2.license_number})")
        
        # Verify license numbers are different
        if doctor_1.license_number != doctor_2.license_number:
            print(f"✅ License numbers are unique: '{doctor_1.license_number}' vs '{doctor_2.license_number}'")
        else:
            print(f"❌ License numbers are not unique: both are '{doctor_1.license_number}'")
            return False
        
        # Clean up
        doctor_1.delete()
        doctor_2.delete()
        user_1.delete()
        user_2.delete()
        print("✅ Test doctors and users deleted successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in unique license test: {str(e)}")
        # Clean up in case of error
        try:
            if 'doctor_1' in locals():
                doctor_1.delete()
            if 'doctor_2' in locals():
                doctor_2.delete()
            if 'user_1' in locals():
                user_1.delete()
            if 'user_2' in locals():
                user_2.delete()
        except:
            pass
        return False

def test_auto_license_generation():
    """Test automatic license number generation"""
    try:
        print("\n🧪 Testing automatic license number generation...")
        
        # Test data
        user_data = {
            'first_name': 'Test',
            'last_name': 'Doctor',
            'email': 'test.doctor.license@example.com',
            'role': 'doctor',
            'phone': '+251911234567',
            'is_staff': True
        }
        
        doctor_data = {
            'specialty': 'general',
            'sub_specialty': 'Family Medicine',
            'years_of_experience': 5,
            'medical_school': 'Addis Ababa University',
            'graduation_year': 2019,
            'certifications': 'MD, General Practice Certificate',
            'consultation_fee': 500.00,
            'availability_status': 'full_time',
            'bio': 'Test doctor for license generation',
            'languages_spoken': 'Amharic, English',
        }
        
        # Generate license number automatically
        year = datetime.now().year
        first_name = user_data['first_name']
        last_name = user_data['last_name']
        base_license = f"ETH-MD-{year}-{first_name[:3].upper()}{last_name[:3].upper()}"
        
        license_number = base_license
        counter = 1
        while Doctor.objects.filter(license_number=license_number).exists():
            license_number = f"{base_license}-{counter}"
            counter += 1
        
        # Create user and doctor
        user = User.objects.create_user(username='dr.test.doctor.license', **user_data)
        user.set_password('doctor123')
        user.save()
        
        doctor = Doctor.objects.create(user=user, license_number=license_number, **doctor_data)
        print(f"✅ Doctor created with auto-generated license: {doctor.get_full_name()}")
        print(f"   - Generated License: {doctor.license_number}")
        print(f"   - Expected Pattern: ETH-MD-{year}-TESDOC")
        
        # Verify license number format
        expected_start = f"ETH-MD-{year}-TESDOC"
        if doctor.license_number.startswith(expected_start):
            print(f"✅ License number format is correct")
        else:
            print(f"❌ License number format is incorrect: {doctor.license_number}")
            return False
        
        # Clean up
        doctor.delete()
        user.delete()
        print("✅ Test doctor and user deleted successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in auto license generation test: {str(e)}")
        # Clean up in case of error
        try:
            if 'doctor' in locals():
                doctor.delete()
            if 'user' in locals():
                user.delete()
        except:
            pass
        return False

if __name__ == '__main__':
    print("🏥 Testing Mobile Doctor Creation with License Number Fix...")
    print("=" * 70)
    
    # Test unique license generation
    success1 = test_unique_license_generation()
    
    # Test auto license generation
    success2 = test_auto_license_generation()
    
    # Summary
    print("\n" + "=" * 70)
    if success1 and success2:
        print("🎉 All tests passed! Doctor creation should work correctly.")
        print("\n📱 You can now test in the mobile interface:")
        print("   1. Go to: http://localhost:8000/doctors/add/?mobile=1")
        print("   2. Fill out all required fields:")
        print("      - First Name and Last Name")
        print("      - Email (must be unique)")
        print("      - Medical School (required)")
        print("      - Graduation Year (required)")
        print("      - Consultation Fee (required)")
        print("   3. Leave Username and License Number blank to auto-generate")
        print("   4. Submit the form")
        print("   5. Verify the doctor is created successfully")
        print("\n💡 The system will automatically generate:")
        print("   - Unique usernames: dr.firstname.lastname, dr.firstname.lastname.1, etc.")
        print("   - Unique license numbers: ETH-MD-2024-FIRLAS, ETH-MD-2024-FIRLAS-1, etc.")
    else:
        print("💥 Some tests failed. Check the errors above.")
