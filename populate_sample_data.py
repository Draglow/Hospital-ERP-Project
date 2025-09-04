#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta, time
from decimal import Decimal
import random
from django.utils import timezone

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_erp.settings')
django.setup()

from accounts.models import User
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from billing.models import Invoice, InvoiceItem
from pharmacy.models import Medicine, Prescription

def create_sample_data():
    """Create comprehensive sample data for the hospital ERP system"""
    
    print("Creating sample data for Ethiopian Hospital ERP...")
    
    # Create sample users (doctors, nurses, etc.)
    users_data = [
        {'username': 'dr_alemayehu', 'first_name': 'Alemayehu', 'last_name': 'Tadesse', 'role': 'doctor', 'email': 'alemayehu@hospital.com'},
        {'username': 'dr_hanan', 'first_name': 'Hanan', 'last_name': 'Mohammed', 'role': 'doctor', 'email': 'hanan@hospital.com'},
        {'username': 'dr_bekele', 'first_name': 'Bekele', 'last_name': 'Worku', 'role': 'doctor', 'email': 'bekele@hospital.com'},
        {'username': 'dr_sara', 'first_name': 'Sara', 'last_name': 'Yohannes', 'role': 'doctor', 'email': 'sara@hospital.com'},
        {'username': 'nurse_meron', 'first_name': 'Meron', 'last_name': 'Getachew', 'role': 'nurse', 'email': 'meron@hospital.com'},
        {'username': 'pharmacist_dawit', 'first_name': 'Dawit', 'last_name': 'Haile', 'role': 'pharmacist', 'email': 'dawit@hospital.com'},
    ]
    
    created_users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'email': user_data['email'],
                'role': user_data['role'],
                'phone': f'+251 91 {random.randint(100, 999)} {random.randint(1000, 9999)}',
                'is_staff': user_data['role'] in ['doctor', 'nurse', 'pharmacist'],
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            created_users.append(user)
            print(f"Created user: {user.get_full_name()} ({user.role})")
    
    # Create sample doctors
    doctors_data = [
        {'user': 'dr_alemayehu', 'specialty': 'cardiology', 'license': 'ETH-DOC-001', 'fee': 500, 'school': 'Addis Ababa University'},
        {'user': 'dr_hanan', 'specialty': 'pediatrics', 'license': 'ETH-DOC-002', 'fee': 400, 'school': 'Jimma University'},
        {'user': 'dr_bekele', 'specialty': 'orthopedics', 'license': 'ETH-DOC-003', 'fee': 600, 'school': 'Mekelle University'},
        {'user': 'dr_sara', 'specialty': 'gynecology', 'license': 'ETH-DOC-004', 'fee': 450, 'school': 'Hawassa University'},
    ]
    
    created_doctors = []
    for doc_data in doctors_data:
        user = User.objects.get(username=doc_data['user'])
        doctor, created = Doctor.objects.get_or_create(
            user=user,
            defaults={
                'license_number': doc_data['license'],
                'specialty': doc_data['specialty'],
                'consultation_fee': doc_data['fee'],
                'medical_school': doc_data['school'],
                'graduation_year': random.randint(2005, 2018),
                'years_of_experience': random.randint(5, 20),
                'monday_start': time(8, 0),
                'monday_end': time(17, 0),
                'tuesday_start': time(8, 0),
                'tuesday_end': time(17, 0),
                'wednesday_start': time(8, 0),
                'wednesday_end': time(17, 0),
                'thursday_start': time(8, 0),
                'thursday_end': time(17, 0),
                'friday_start': time(8, 0),
                'friday_end': time(17, 0),
            }
        )
        if created:
            created_doctors.append(doctor)
            print(f"Created doctor: Dr. {doctor.user.get_full_name()} - {doctor.get_specialty_display()}")
    
    # Create sample patients
    patients_data = [
        {'first_name': 'Alemayehu', 'last_name': 'Tadesse', 'gender': 'M', 'city': 'Addis Ababa', 'kebele': 'Kebele 01', 'woreda': 'Bole'},
        {'first_name': 'Hanan', 'last_name': 'Mohammed', 'gender': 'F', 'city': 'Addis Ababa', 'kebele': 'Kebele 02', 'woreda': 'Kirkos'},
        {'first_name': 'Bekele', 'last_name': 'Worku', 'gender': 'M', 'city': 'Bahir Dar', 'kebele': 'Kebele 03', 'woreda': 'Bahir Dar Zuria'},
        {'first_name': 'Sara', 'last_name': 'Yohannes', 'gender': 'F', 'city': 'Mekelle', 'kebele': 'Kebele 04', 'woreda': 'Quiha'},
        {'first_name': 'Dawit', 'last_name': 'Haile', 'gender': 'M', 'city': 'Hawassa', 'kebele': 'Kebele 05', 'woreda': 'Hawassa Zuria'},
        {'first_name': 'Meron', 'last_name': 'Getachew', 'gender': 'F', 'city': 'Dire Dawa', 'kebele': 'Kebele 06', 'woreda': 'Dire Dawa'},
        {'first_name': 'Yonas', 'last_name': 'Tesfaye', 'gender': 'M', 'city': 'Adama', 'kebele': 'Kebele 07', 'woreda': 'Adama'},
        {'first_name': 'Tigist', 'last_name': 'Alemu', 'gender': 'F', 'city': 'Gondar', 'kebele': 'Kebele 08', 'woreda': 'Gondar Zuria'},
    ]
    
    created_patients = []
    for i, patient_data in enumerate(patients_data):
        birth_date = datetime.now().date() - timedelta(days=random.randint(18*365, 70*365))
        patient, created = Patient.objects.get_or_create(
            first_name=patient_data['first_name'],
            last_name=patient_data['last_name'],
            defaults={
                'date_of_birth': birth_date,
                'gender': patient_data['gender'],
                'kebele': patient_data['kebele'],
                'woreda': patient_data['woreda'],
                'city': patient_data['city'],
                'region': 'Addis Ababa' if patient_data['city'] == 'Addis Ababa' else 'Other',
                'phone': f'+251 91 {random.randint(100, 999)} {random.randint(1000, 9999)}',
                'email': f"{patient_data['first_name'].lower()}@email.com",
                'emergency_contact_name': f"Emergency Contact {i+1}",
                'emergency_contact_phone': f'+251 92 {random.randint(100, 999)} {random.randint(1000, 9999)}',
                'emergency_contact_relationship': random.choice(['Spouse', 'Parent', 'Sibling', 'Child']),
                'blood_type': random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
            }
        )
        if created:
            created_patients.append(patient)
            print(f"Created patient: {patient.get_full_name()} - {patient.patient_id}")
    
    # Create sample medicines
    medicines_data = [
        {'name': 'Paracetamol', 'category': 'painkiller', 'form': 'tablet', 'strength': '500mg', 'price': 5.50},
        {'name': 'Amoxicillin', 'category': 'antibiotic', 'form': 'capsule', 'strength': '250mg', 'price': 12.00},
        {'name': 'Ibuprofen', 'category': 'painkiller', 'form': 'tablet', 'strength': '400mg', 'price': 8.75},
        {'name': 'Vitamin C', 'category': 'vitamin', 'form': 'tablet', 'strength': '1000mg', 'price': 15.00},
        {'name': 'Metformin', 'category': 'diabetes', 'form': 'tablet', 'strength': '500mg', 'price': 25.00},
        {'name': 'Aspirin', 'category': 'cardiac', 'form': 'tablet', 'strength': '75mg', 'price': 6.25},
        {'name': 'Cough Syrup', 'category': 'respiratory', 'form': 'syrup', 'strength': '100ml', 'price': 18.50},
        {'name': 'Eye Drops', 'category': 'ophthalmological', 'form': 'drops', 'strength': '10ml', 'price': 22.00},
    ]
    
    created_medicines = []
    for med_data in medicines_data:
        expiry_date = datetime.now().date() + timedelta(days=random.randint(365, 1095))  # 1-3 years
        medicine, created = Medicine.objects.get_or_create(
            name=med_data['name'],
            defaults={
                'category': med_data['category'],
                'form': med_data['form'],
                'strength': med_data['strength'],
                'manufacturer': f"Ethiopian Pharmaceuticals {random.randint(1, 5)}",
                'stock_quantity': random.randint(50, 500),
                'minimum_stock_level': random.randint(10, 50),
                'unit_price': Decimal(str(med_data['price'])),
                'cost_price': Decimal(str(med_data['price'] * 0.7)),
                'expiry_date': expiry_date,
            }
        )
        if created:
            created_medicines.append(medicine)
            print(f"Created medicine: {medicine.name} - {medicine.strength}")
    
    print(f"\nSample data creation completed!")
    print(f"Created {len(created_users)} users")
    print(f"Created {len(created_doctors)} doctors")
    print(f"Created {len(created_patients)} patients")
    print(f"Created {len(created_medicines)} medicines")
    print("\nYou can now explore the fully functional Ethiopian Hospital ERP system!")

if __name__ == '__main__':
    create_sample_data()
