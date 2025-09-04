#!/usr/bin/env python
"""
Test script to verify doctor creation with unique username generation works correctly
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

def test_unique_username_generation():
    """Test creating multiple doctors with same names to verify unique username generation"""
    try:
        print("🧪 Testing unique username generation...")
        
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
            'license_number': 'ETH-MD-2024-001',
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
        
        # Create first doctor with base username
        base_username = 'dr.john.smith'
        username_1 = base_username
        counter = 1
        while User.objects.filter(username=username_1).exists():
            username_1 = f"{base_username}.{counter}"
            counter += 1
        
        user_1 = User.objects.create_user(username=username_1, **user_data_1)
        user_1.set_password('doctor123')
        user_1.save()
        
        doctor_1 = Doctor.objects.create(user=user_1, **doctor_data_1)
        print(f"✅ First doctor created: {doctor_1.get_full_name()} (username: {user_1.username})")
        
        # Test data for second doctor with same name
        user_data_2 = {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john.smith2@example.com',
            'role': 'doctor',
            'phone': '+251911234568',
            'is_staff': True
        }
        
        doctor_data_2 = {
            'license_number': 'ETH-MD-2024-002',
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
        
        # Create second doctor - should get unique username
        username_2 = base_username
        counter = 1
        while User.objects.filter(username=username_2).exists():
            username_2 = f"{base_username}.{counter}"
            counter += 1
        
        user_2 = User.objects.create_user(username=username_2, **user_data_2)
        user_2.set_password('doctor123')
        user_2.save()
        
        doctor_2 = Doctor.objects.create(user=user_2, **doctor_data_2)
        print(f"✅ Second doctor created: {doctor_2.get_full_name()} (username: {user_2.username})")
        
        # Verify usernames are different
        if user_1.username != user_2.username:
            print(f"✅ Usernames are unique: '{user_1.username}' vs '{user_2.username}'")
        else:
            print(f"❌ Usernames are not unique: both are '{user_1.username}'")
            return False
        
        # Clean up
        doctor_1.delete()
        doctor_2.delete()
        user_1.delete()
        user_2.delete()
        print("✅ Test doctors and users deleted successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in unique username test: {str(e)}")
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

def test_complete_doctor_creation():
    """Test creating a complete doctor with all required fields"""
    try:
        print("\n🧪 Testing complete doctor creation...")
        
        # Test data
        user_data = {
            'first_name': 'Test',
            'last_name': 'Doctor',
            'email': 'test.doctor@example.com',
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
        
        # Generate unique username
        base_username = 'dr.test.doctor'
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}.{counter}"
            counter += 1
        
        # Create user and doctor
        user = User.objects.create_user(username=username, **user_data)
        user.set_password('doctor123')
        user.save()
        
        doctor = Doctor.objects.create(user=user, **doctor_data)
        print(f"✅ Doctor created successfully: {doctor.get_full_name()} (username: {user.username})")
        
        # Verify all required fields
        print(f"   - Medical School: {doctor.medical_school}")
        print(f"   - Graduation Year: {doctor.graduation_year}")
        print(f"   - License Number: {doctor.license_number}")
        print(f"   - Consultation Fee: {doctor.consultation_fee} ETB")
        print(f"   - Specialty: {doctor.get_specialty_display()}")
        
        # Clean up
        doctor.delete()
        user.delete()
        print("✅ Test doctor and user deleted successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating complete doctor: {str(e)}")
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
    print("🏥 Testing Mobile Doctor Creation with Username Fix...")
    print("=" * 60)
    
    # Test unique username generation
    success1 = test_unique_username_generation()
    
    # Test complete doctor creation
    success2 = test_complete_doctor_creation()
    
    # Summary
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 All tests passed! Doctor creation should work correctly.")
        print("\n📱 You can now test in the mobile interface:")
        print("   1. Go to: http://localhost:8000/doctors/add/?mobile=1")
        print("   2. Fill out all required fields:")
        print("      - First Name and Last Name")
        print("      - Email (must be unique)")
        print("      - Medical School (required)")
        print("      - Graduation Year (required)")
        print("      - License Number (required)")
        print("      - Consultation Fee (required)")
        print("   3. Leave Username blank to auto-generate")
        print("   4. Submit the form")
        print("   5. Verify the doctor is created successfully")
        print("\n💡 The system will automatically generate unique usernames!")
    else:
        print("💥 Some tests failed. Check the errors above.")
