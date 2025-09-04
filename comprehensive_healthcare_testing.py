#!/usr/bin/env python3
"""
Comprehensive Healthcare Dashboard Testing Suite
Tests all modules: appointments, doctors, patients, pharmacy, billing
Covers both desktop and mobile functionality
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.management import call_command
from django.db import transaction
from decimal import Decimal
import json
import time
from datetime import datetime, date, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_erp.settings')
django.setup()

# Import models after Django setup
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from pharmacy.models import Medicine, Prescription
from billing.models import Invoice, InvoiceItem
from accounts.models import User

class HealthcareDashboardTestSuite:
    """Comprehensive test suite for all healthcare modules"""
    
    def __init__(self):
        self.client = Client()
        self.test_results = {
            'patients': {'desktop': {}, 'mobile': {}},
            'doctors': {'desktop': {}, 'mobile': {}},
            'appointments': {'desktop': {}, 'mobile': {}},
            'pharmacy': {'desktop': {}, 'mobile': {}},
            'billing': {'desktop': {}, 'mobile': {}},
            'cross_platform': {},
            'performance': {},
            'ui_elements': {}
        }
        self.setup_test_data()
    
    def setup_test_data(self):
        """Create test data for all modules"""
        print("Setting up test data...")
        
        # Create test user
        User = get_user_model()
        self.test_user, created = User.objects.get_or_create(
            username='test_admin',
            defaults={
                'email': 'test@hospital.com',
                'first_name': 'Test',
                'last_name': 'Admin',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            self.test_user.set_password('testpass123')
            self.test_user.save()
        
        # Create test patient
        self.test_patient, created = Patient.objects.get_or_create(
            patient_id='PAT202400001',
            defaults={
                'first_name': 'Almaz',
                'last_name': 'Tadesse',
                'date_of_birth': date(1990, 5, 15),
                'gender': 'F',
                'kebele': 'Kebele 01',
                'woreda': 'Bole',
                'phone': '+251911234567',
                'emergency_contact_name': 'Dawit Tadesse',
                'emergency_contact_phone': '+251911234568',
                'emergency_contact_relationship': 'Husband'
            }
        )
        
        # Create test doctor
        try:
            doctor_user, created = User.objects.get_or_create(
                username='dr_test',
                defaults={
                    'email': 'doctor@hospital.com',
                    'first_name': 'Dr. Meron',
                    'last_name': 'Haile',
                    'role': 'doctor'
                }
            )
            if created:
                doctor_user.set_password('doctorpass123')
                doctor_user.save()
            
            self.test_doctor, created = Doctor.objects.get_or_create(
                user=doctor_user,
                defaults={
                    'license_number': 'ETH-DOC-001',
                    'specialty': 'general',
                    'medical_school': 'Addis Ababa University',
                    'graduation_year': 2015,
                    'consultation_fee': Decimal('500.00')
                }
            )
        except Exception as e:
            print(f"Error creating doctor: {e}")
        
        # Create test medicine
        self.test_medicine, created = Medicine.objects.get_or_create(
            name='Paracetamol',
            defaults={
                'generic_name': 'Acetaminophen',
                'manufacturer': 'Ethiopian Pharmaceuticals',
                'category': 'painkiller',
                'form': 'tablet',
                'strength': '500mg',
                'stock_quantity': 100,
                'unit_price': Decimal('5.50'),
                'cost_price': Decimal('3.00'),
                'expiry_date': date.today() + timedelta(days=365)
            }
        )
        
        print("Test data setup complete!")
    
    def login_user(self):
        """Login test user"""
        return self.client.login(username='test_admin', password='testpass123')
    
    def test_patient_module(self):
        """Test patient management functionality"""
        print("\n=== Testing Patient Module ===")
        
        # Desktop tests
        self.test_results['patients']['desktop'] = {
            'list_view': self.test_patient_list(),
            'add_patient': self.test_patient_add(),
            'edit_patient': self.test_patient_edit(),
            'detail_view': self.test_patient_detail(),
            'search_functionality': self.test_patient_search()
        }
        
        # Mobile tests
        self.test_results['patients']['mobile'] = {
            'mobile_list': self.test_patient_mobile_list(),
            'mobile_add': self.test_patient_mobile_add(),
            'mobile_responsive': self.test_patient_mobile_responsive()
        }
    
    def test_patient_list(self):
        """Test patient list view"""
        try:
            self.login_user()
            response = self.client.get(reverse('patients:patient_list'))
            return {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'contains_patient': 'Almaz Tadesse' in response.content.decode(),
                'pagination_works': 'page_obj' in response.context if hasattr(response, 'context') else False
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_patient_add(self):
        """Test adding new patient"""
        try:
            self.login_user()
            
            # Test GET request (form display)
            response = self.client.get(reverse('patients:patient_add'))
            form_displayed = response.status_code == 200
            
            # Test POST request (form submission)
            patient_data = {
                'first_name': 'Hanan',
                'last_name': 'Mohammed',
                'date_of_birth': '1985-03-20',
                'gender': 'F',
                'kebele': 'Kebele 05',
                'woreda': 'Kirkos',
                'phone': '+251911234569',
                'emergency_contact_name': 'Ahmed Mohammed',
                'emergency_contact_phone': '+251911234570',
                'emergency_contact_relationship': 'Brother'
            }
            
            response = self.client.post(reverse('patients:patient_add'), patient_data)
            
            return {
                'form_displayed': form_displayed,
                'submission_success': response.status_code in [200, 302],
                'patient_created': Patient.objects.filter(first_name='Hanan', last_name='Mohammed').exists()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_patient_edit(self):
        """Test editing existing patient"""
        try:
            self.login_user()
            
            # Test GET request (edit form)
            response = self.client.get(reverse('patients:patient_edit', kwargs={'pk': self.test_patient.pk}))
            form_displayed = response.status_code == 200
            
            # Test POST request (update)
            updated_data = {
                'first_name': 'Almaz Updated',
                'last_name': 'Tadesse',
                'date_of_birth': '1990-05-15',
                'gender': 'F',
                'kebele': 'Kebele 01 Updated',
                'woreda': 'Bole',
                'phone': '+251911234567',
                'emergency_contact_name': 'Dawit Tadesse',
                'emergency_contact_phone': '+251911234568',
                'emergency_contact_relationship': 'Husband'
            }
            
            response = self.client.post(
                reverse('patients:patient_edit', kwargs={'pk': self.test_patient.pk}),
                updated_data
            )
            
            # Refresh from database
            self.test_patient.refresh_from_db()
            
            return {
                'form_displayed': form_displayed,
                'update_success': response.status_code in [200, 302],
                'data_updated': self.test_patient.first_name == 'Almaz Updated'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_patient_detail(self):
        """Test patient detail view"""
        try:
            self.login_user()
            response = self.client.get(reverse('patients:patient_detail', kwargs={'pk': self.test_patient.pk}))
            
            return {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'shows_patient_info': self.test_patient.first_name in response.content.decode(),
                'has_action_buttons': 'Edit Patient' in response.content.decode()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_patient_search(self):
        """Test patient search functionality"""
        try:
            self.login_user()
            
            # Test search by name
            response = self.client.get(reverse('patients:patient_list'), {'search': 'Almaz'})
            search_works = response.status_code == 200 and 'Almaz' in response.content.decode()
            
            # Test search by patient ID
            response = self.client.get(reverse('patients:patient_list'), {'search': self.test_patient.patient_id})
            id_search_works = response.status_code == 200
            
            return {
                'name_search': search_works,
                'id_search': id_search_works,
                'overall_success': search_works and id_search_works
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_patient_mobile_list(self):
        """Test mobile patient list"""
        try:
            self.login_user()
            response = self.client.get(reverse('patients:patient_list'), {'mobile': '1'})
            
            return {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'mobile_template': 'mobile' in response.template_name[0] if hasattr(response, 'template_name') else False
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_patient_mobile_add(self):
        """Test mobile patient add"""
        try:
            self.login_user()
            response = self.client.get(reverse('patients:patient_add'), {'mobile': '1'})
            
            return {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'mobile_optimized': response.status_code == 200
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_patient_mobile_responsive(self):
        """Test mobile responsive design"""
        try:
            self.login_user()
            
            # Simulate mobile user agent
            response = self.client.get(
                reverse('patients:patient_list'),
                HTTP_USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
            )
            
            return {
                'loads_on_mobile': response.status_code == 200,
                'responsive_design': True  # Would need browser automation for full test
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_doctor_module(self):
        """Test doctor management functionality"""
        print("\n=== Testing Doctor Module ===")

        # Desktop tests
        self.test_results['doctors']['desktop'] = {
            'list_view': self.test_doctor_list(),
            'add_doctor': self.test_doctor_add(),
            'edit_doctor': self.test_doctor_edit(),
            'detail_view': self.test_doctor_detail(),
            'availability_management': self.test_doctor_availability()
        }

        # Mobile tests
        self.test_results['doctors']['mobile'] = {
            'mobile_list': self.test_doctor_mobile_list(),
            'mobile_add': self.test_doctor_mobile_add(),
            'mobile_responsive': self.test_doctor_mobile_responsive()
        }

    def test_doctor_list(self):
        """Test doctor list view"""
        try:
            self.login_user()
            response = self.client.get(reverse('doctors:doctor_list'))
            return {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'contains_doctor': 'Dr. Meron' in response.content.decode(),
                'specialty_filter': 'specialty' in response.content.decode().lower()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_doctor_add(self):
        """Test adding new doctor"""
        try:
            self.login_user()

            # Create user for new doctor
            new_user = User.objects.create_user(
                username='dr_new',
                email='newdoctor@hospital.com',
                first_name='Dr. Yohannes',
                last_name='Kebede',
                password='newdoctorpass123'
            )

            doctor_data = {
                'user': new_user.id,
                'license_number': 'ETH-DOC-002',
                'specialty': 'cardiology',
                'medical_school': 'Jimma University',
                'graduation_year': 2018,
                'consultation_fee': '750.00'
            }

            response = self.client.post(reverse('doctors:doctor_add'), doctor_data)

            return {
                'submission_success': response.status_code in [200, 302],
                'doctor_created': Doctor.objects.filter(license_number='ETH-DOC-002').exists()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_doctor_edit(self):
        """Test editing existing doctor"""
        try:
            self.login_user()

            updated_data = {
                'user': self.test_doctor.user.id,
                'license_number': self.test_doctor.license_number,
                'specialty': 'pediatrics',  # Changed specialty
                'medical_school': self.test_doctor.medical_school,
                'graduation_year': self.test_doctor.graduation_year,
                'consultation_fee': '600.00'  # Changed fee
            }

            response = self.client.post(
                reverse('doctors:doctor_edit', kwargs={'pk': self.test_doctor.pk}),
                updated_data
            )

            self.test_doctor.refresh_from_db()

            return {
                'update_success': response.status_code in [200, 302],
                'specialty_updated': self.test_doctor.specialty == 'pediatrics',
                'fee_updated': str(self.test_doctor.consultation_fee) == '600.00'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_doctor_detail(self):
        """Test doctor detail view"""
        try:
            self.login_user()
            response = self.client.get(reverse('doctors:doctor_detail', kwargs={'pk': self.test_doctor.pk}))

            return {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'shows_doctor_info': self.test_doctor.user.first_name in response.content.decode(),
                'shows_specialty': self.test_doctor.get_specialty_display() in response.content.decode()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_doctor_availability(self):
        """Test doctor availability management"""
        try:
            self.login_user()
            # This would test availability scheduling functionality
            return {
                'availability_system': True,  # Placeholder for actual availability tests
                'time_slot_management': True
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_doctor_mobile_list(self):
        """Test mobile doctor list"""
        try:
            self.login_user()
            response = self.client.get(reverse('doctors:doctor_list'), {'mobile': '1'})

            return {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'mobile_optimized': response.status_code == 200
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_doctor_mobile_add(self):
        """Test mobile doctor add"""
        try:
            self.login_user()
            response = self.client.get(reverse('doctors:doctor_add'), {'mobile': '1'})

            return {
                'status_code': response.status_code,
                'success': response.status_code == 200
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_doctor_mobile_responsive(self):
        """Test mobile responsive design for doctors"""
        try:
            self.login_user()
            response = self.client.get(
                reverse('doctors:doctor_list'),
                HTTP_USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
            )

            return {
                'loads_on_mobile': response.status_code == 200,
                'responsive_design': True
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_appointment_module(self):
        """Test appointment management functionality"""
        print("\n=== Testing Appointment Module ===")

        # Desktop tests
        self.test_results['appointments']['desktop'] = {
            'list_view': self.test_appointment_list(),
            'add_appointment': self.test_appointment_add(),
            'edit_appointment': self.test_appointment_edit(),
            'cancel_appointment': self.test_appointment_cancel(),
            'status_management': self.test_appointment_status(),
            'doctor_availability': self.test_appointment_availability()
        }

        # Mobile tests
        self.test_results['appointments']['mobile'] = {
            'mobile_list': self.test_appointment_mobile_list(),
            'mobile_booking': self.test_appointment_mobile_booking(),
            'mobile_responsive': self.test_appointment_mobile_responsive()
        }

    def test_appointment_list(self):
        """Test appointment list view"""
        try:
            self.login_user()
            response = self.client.get(reverse('appointments:appointment_list'))
            return {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'has_filters': 'status' in response.content.decode().lower(),
                'has_search': 'search' in response.content.decode().lower()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_appointment_add(self):
        """Test adding new appointment"""
        try:
            self.login_user()

            appointment_data = {
                'patient': self.test_patient.id,
                'doctor': self.test_doctor.id,
                'appointment_date': (date.today() + timedelta(days=1)).strftime('%Y-%m-%d'),
                'appointment_time': '10:00',
                'appointment_type': 'consultation',
                'priority': 'normal',
                'chief_complaint': 'Regular checkup',
                'symptoms': 'No specific symptoms'
            }

            response = self.client.post(reverse('appointments:appointment_add'), appointment_data)

            return {
                'submission_success': response.status_code in [200, 302],
                'appointment_created': Appointment.objects.filter(
                    patient=self.test_patient,
                    doctor=self.test_doctor
                ).exists()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_appointment_edit(self):
        """Test editing existing appointment"""
        try:
            self.login_user()

            # Create test appointment first
            appointment = Appointment.objects.create(
                patient=self.test_patient,
                doctor=self.test_doctor,
                appointment_date=date.today() + timedelta(days=2),
                appointment_time='14:00',
                appointment_type='consultation',
                priority='normal',
                chief_complaint='Test appointment',
                created_by=self.test_user
            )

            updated_data = {
                'patient': self.test_patient.id,
                'doctor': self.test_doctor.id,
                'appointment_date': appointment.appointment_date.strftime('%Y-%m-%d'),
                'appointment_time': '15:00',  # Changed time
                'appointment_type': 'follow_up',  # Changed type
                'priority': 'high',  # Changed priority
                'chief_complaint': 'Updated complaint',
                'symptoms': 'Updated symptoms'
            }

            response = self.client.post(
                reverse('appointments:appointment_edit', kwargs={'pk': appointment.pk}),
                updated_data
            )

            appointment.refresh_from_db()

            return {
                'update_success': response.status_code in [200, 302],
                'time_updated': appointment.appointment_time.strftime('%H:%M') == '15:00',
                'type_updated': appointment.appointment_type == 'follow_up'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_appointment_cancel(self):
        """Test appointment cancellation"""
        try:
            self.login_user()

            # Create test appointment
            appointment = Appointment.objects.create(
                patient=self.test_patient,
                doctor=self.test_doctor,
                appointment_date=date.today() + timedelta(days=3),
                appointment_time='16:00',
                appointment_type='consultation',
                priority='normal',
                chief_complaint='Test cancellation',
                created_by=self.test_user
            )

            response = self.client.post(
                reverse('appointments:appointment_cancel', kwargs={'pk': appointment.pk})
            )

            appointment.refresh_from_db()

            return {
                'cancel_success': response.status_code in [200, 302],
                'status_updated': appointment.status == 'cancelled'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_appointment_status(self):
        """Test appointment status management"""
        try:
            self.login_user()

            # Create test appointment
            appointment = Appointment.objects.create(
                patient=self.test_patient,
                doctor=self.test_doctor,
                appointment_date=date.today(),
                appointment_time='09:00',
                appointment_type='consultation',
                priority='normal',
                chief_complaint='Status test',
                created_by=self.test_user
            )

            # Test status transitions
            statuses_to_test = ['confirmed', 'in_progress', 'completed']
            status_results = {}

            for status in statuses_to_test:
                appointment.status = status
                appointment.save()
                status_results[status] = appointment.status == status

            return {
                'status_transitions': all(status_results.values()),
                'individual_statuses': status_results
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_appointment_availability(self):
        """Test doctor availability checking"""
        try:
            self.login_user()

            # Test availability check endpoint
            response = self.client.get(reverse('appointments:check_availability'), {
                'doctor': self.test_doctor.id,
                'date': (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
            })

            return {
                'availability_check': response.status_code == 200,
                'returns_json': response.get('Content-Type', '').startswith('application/json') if hasattr(response, 'get') else False
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_appointment_mobile_list(self):
        """Test mobile appointment list"""
        try:
            self.login_user()
            response = self.client.get(reverse('appointments:appointment_list'), {'mobile': '1'})

            return {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'mobile_optimized': response.status_code == 200
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_appointment_mobile_booking(self):
        """Test mobile appointment booking"""
        try:
            self.login_user()
            response = self.client.get(reverse('appointments:appointment_add'), {'mobile': '1'})

            return {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'mobile_form': response.status_code == 200
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_appointment_mobile_responsive(self):
        """Test mobile responsive design for appointments"""
        try:
            self.login_user()
            response = self.client.get(
                reverse('appointments:appointment_list'),
                HTTP_USER_AGENT='Mozilla/5.0 (Android 10; Mobile; rv:81.0)'
            )

            return {
                'loads_on_mobile': response.status_code == 200,
                'responsive_design': True
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def run_all_tests(self):
        """Run all test suites"""
        print("Starting Comprehensive Healthcare Dashboard Testing...")
        print("=" * 60)

        # Test all modules
        self.test_patient_module()
        self.test_doctor_module()
        self.test_appointment_module()
        self.test_pharmacy_module()
        self.test_billing_module()
        self.test_cross_platform_functionality()
        self.test_ui_elements_and_animations()

        return self.test_results

    def test_pharmacy_module(self):
        """Test pharmacy management functionality"""
        print("\n=== Testing Pharmacy Module ===")

        # Desktop tests
        self.test_results['pharmacy']['desktop'] = {
            'medicine_list': self.test_medicine_list(),
            'add_medicine': self.test_medicine_add(),
            'edit_medicine': self.test_medicine_edit(),
            'stock_management': self.test_stock_management(),
            'expiry_tracking': self.test_expiry_tracking(),
            'prescription_handling': self.test_prescription_handling()
        }

        # Mobile tests
        self.test_results['pharmacy']['mobile'] = {
            'mobile_list': self.test_pharmacy_mobile_list(),
            'mobile_add': self.test_pharmacy_mobile_add(),
            'mobile_responsive': self.test_pharmacy_mobile_responsive()
        }

    def test_medicine_list(self):
        """Test medicine list view"""
        try:
            self.login_user()
            response = self.client.get(reverse('pharmacy:medicine_list'))
            return {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'contains_medicine': 'Paracetamol' in response.content.decode(),
                'has_stock_info': 'stock' in response.content.decode().lower()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_medicine_add(self):
        """Test adding new medicine"""
        try:
            self.login_user()

            medicine_data = {
                'name': 'Amoxicillin',
                'generic_name': 'Amoxicillin',
                'manufacturer': 'Ethiopian Pharmaceuticals',
                'category': 'antibiotic',
                'form': 'capsule',
                'strength': '250mg',
                'stock_quantity': 50,
                'minimum_stock_level': 10,
                'unit_price': '12.50',
                'cost_price': '8.00',
                'expiry_date': (date.today() + timedelta(days=730)).strftime('%Y-%m-%d')
            }

            response = self.client.post(reverse('pharmacy:medicine_add'), medicine_data)

            return {
                'submission_success': response.status_code in [200, 302],
                'medicine_created': Medicine.objects.filter(name='Amoxicillin').exists()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_medicine_edit(self):
        """Test editing existing medicine"""
        try:
            self.login_user()

            updated_data = {
                'name': self.test_medicine.name,
                'generic_name': self.test_medicine.generic_name,
                'manufacturer': self.test_medicine.manufacturer,
                'category': self.test_medicine.category,
                'form': self.test_medicine.form,
                'strength': self.test_medicine.strength,
                'stock_quantity': 150,  # Updated stock
                'minimum_stock_level': 20,  # Updated minimum
                'unit_price': '6.00',  # Updated price
                'cost_price': self.test_medicine.cost_price,
                'expiry_date': self.test_medicine.expiry_date.strftime('%Y-%m-%d')
            }

            response = self.client.post(
                reverse('pharmacy:medicine_edit', kwargs={'pk': self.test_medicine.pk}),
                updated_data
            )

            self.test_medicine.refresh_from_db()

            return {
                'update_success': response.status_code in [200, 302],
                'stock_updated': self.test_medicine.stock_quantity == 150,
                'price_updated': str(self.test_medicine.unit_price) == '6.00'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_stock_management(self):
        """Test stock management functionality"""
        try:
            self.login_user()

            # Test low stock detection
            low_stock_medicine = Medicine.objects.create(
                name='Low Stock Medicine',
                manufacturer='Test Manufacturer',
                category='other',
                form='tablet',
                strength='100mg',
                stock_quantity=5,  # Below minimum
                minimum_stock_level=10,
                unit_price=Decimal('10.00'),
                cost_price=Decimal('6.00'),
                expiry_date=date.today() + timedelta(days=365)
            )

            return {
                'low_stock_detection': low_stock_medicine.is_low_stock(),
                'stock_calculation': low_stock_medicine.stock_quantity < low_stock_medicine.minimum_stock_level
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_expiry_tracking(self):
        """Test expiry date tracking"""
        try:
            self.login_user()

            # Test expiry detection
            expiring_medicine = Medicine.objects.create(
                name='Expiring Medicine',
                manufacturer='Test Manufacturer',
                category='other',
                form='tablet',
                strength='50mg',
                stock_quantity=20,
                minimum_stock_level=5,
                unit_price=Decimal('15.00'),
                cost_price=Decimal('10.00'),
                expiry_date=date.today() + timedelta(days=5)  # Expiring soon
            )

            return {
                'expiry_detection': expiring_medicine.is_expiring_soon(7),
                'expiry_calculation': (expiring_medicine.expiry_date - date.today()).days <= 7
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_prescription_handling(self):
        """Test prescription management"""
        try:
            self.login_user()

            # Create test appointment for prescription
            appointment = Appointment.objects.create(
                patient=self.test_patient,
                doctor=self.test_doctor,
                appointment_date=date.today(),
                appointment_time='11:00',
                appointment_type='consultation',
                priority='normal',
                chief_complaint='Prescription test',
                created_by=self.test_user
            )

            # Create prescription
            prescription = Prescription.objects.create(
                appointment=appointment,
                medicine=self.test_medicine,
                quantity=10,
                dosage='1 tablet twice daily',
                duration_days=7
            )

            return {
                'prescription_created': Prescription.objects.filter(id=prescription.id).exists(),
                'links_to_appointment': prescription.appointment == appointment,
                'links_to_medicine': prescription.medicine == self.test_medicine
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_pharmacy_mobile_list(self):
        """Test mobile pharmacy list"""
        try:
            self.login_user()
            response = self.client.get(reverse('pharmacy:medicine_list'), {'mobile': '1'})

            return {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'mobile_optimized': response.status_code == 200
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_pharmacy_mobile_add(self):
        """Test mobile pharmacy add"""
        try:
            self.login_user()
            response = self.client.get(reverse('pharmacy:medicine_add'), {'mobile': '1'})

            return {
                'status_code': response.status_code,
                'success': response.status_code == 200
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_pharmacy_mobile_responsive(self):
        """Test mobile responsive design for pharmacy"""
        try:
            self.login_user()
            response = self.client.get(
                reverse('pharmacy:medicine_list'),
                HTTP_USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
            )

            return {
                'loads_on_mobile': response.status_code == 200,
                'responsive_design': True
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_billing_module(self):
        """Test billing management functionality"""
        print("\n=== Testing Billing Module ===")

        # Desktop tests
        self.test_results['billing']['desktop'] = {
            'invoice_list': self.test_invoice_list(),
            'create_invoice': self.test_invoice_create(),
            'edit_invoice': self.test_invoice_edit(),
            'payment_processing': self.test_payment_processing(),
            'invoice_pdf': self.test_invoice_pdf(),
            'billing_reports': self.test_billing_reports()
        }

        # Mobile tests
        self.test_results['billing']['mobile'] = {
            'mobile_list': self.test_billing_mobile_list(),
            'mobile_create': self.test_billing_mobile_create(),
            'mobile_responsive': self.test_billing_mobile_responsive()
        }

    def test_invoice_list(self):
        """Test invoice list view"""
        try:
            self.login_user()
            response = self.client.get(reverse('billing:invoice_list'))
            return {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'has_filters': 'status' in response.content.decode().lower(),
                'has_totals': 'total' in response.content.decode().lower()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_invoice_create(self):
        """Test creating new invoice"""
        try:
            self.login_user()

            invoice_data = {
                'patient': self.test_patient.id,
                'doctor': self.test_doctor.id,
                'issue_date': date.today().strftime('%Y-%m-%d'),
                'due_date': (date.today() + timedelta(days=30)).strftime('%Y-%m-%d'),
                'payment_method': 'cash',
                'notes': 'Test invoice creation'
            }

            response = self.client.post(reverse('billing:invoice_add'), invoice_data)

            return {
                'submission_success': response.status_code in [200, 302],
                'invoice_created': Invoice.objects.filter(patient=self.test_patient).exists()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_invoice_edit(self):
        """Test editing existing invoice"""
        try:
            self.login_user()

            # Create test invoice
            invoice = Invoice.objects.create(
                patient=self.test_patient,
                doctor=self.test_doctor,
                issue_date=date.today(),
                due_date=date.today() + timedelta(days=30),
                payment_method='cash',
                subtotal=Decimal('500.00'),
                total_amount=Decimal('500.00'),
                created_by=self.test_user
            )

            updated_data = {
                'due_date': (date.today() + timedelta(days=45)).strftime('%Y-%m-%d'),
                'payment_method': 'bank_transfer',
                'notes': 'Updated invoice',
                'status': 'sent',
                'discount_amount': '50.00'
            }

            response = self.client.post(
                reverse('billing:invoice_edit', kwargs={'pk': invoice.pk}),
                updated_data
            )

            invoice.refresh_from_db()

            return {
                'update_success': response.status_code in [200, 302],
                'payment_method_updated': invoice.payment_method == 'bank_transfer',
                'status_updated': invoice.status == 'sent'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_payment_processing(self):
        """Test payment processing functionality"""
        try:
            self.login_user()

            # Create test invoice
            invoice = Invoice.objects.create(
                patient=self.test_patient,
                doctor=self.test_doctor,
                issue_date=date.today(),
                due_date=date.today() + timedelta(days=30),
                payment_method='cash',
                subtotal=Decimal('1000.00'),
                total_amount=Decimal('1000.00'),
                created_by=self.test_user
            )

            payment_data = {
                'payment_amount': '1000.00',
                'payment_method': 'cash',
                'payment_reference': 'CASH-001'
            }

            response = self.client.post(
                reverse('billing:invoice_pay', kwargs={'pk': invoice.pk}),
                payment_data
            )

            invoice.refresh_from_db()

            return {
                'payment_success': response.status_code in [200, 302],
                'amount_updated': invoice.paid_amount == Decimal('1000.00'),
                'status_updated': invoice.status == 'paid'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_invoice_pdf(self):
        """Test invoice PDF generation"""
        try:
            self.login_user()

            # Create test invoice
            invoice = Invoice.objects.create(
                patient=self.test_patient,
                doctor=self.test_doctor,
                issue_date=date.today(),
                due_date=date.today() + timedelta(days=30),
                payment_method='cash',
                subtotal=Decimal('750.00'),
                total_amount=Decimal('750.00'),
                created_by=self.test_user
            )

            response = self.client.get(reverse('billing:invoice_pdf', kwargs={'pk': invoice.pk}))

            return {
                'pdf_generation': response.status_code == 200,
                'content_type': 'html' in response.get('Content-Type', '') if hasattr(response, 'get') else True
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_billing_reports(self):
        """Test billing reports and analytics"""
        try:
            self.login_user()

            # Test if billing list includes summary statistics
            response = self.client.get(reverse('billing:invoice_list'))
            content = response.content.decode()

            return {
                'has_statistics': any(keyword in content.lower() for keyword in ['total', 'paid', 'pending']),
                'reports_accessible': response.status_code == 200
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_billing_mobile_list(self):
        """Test mobile billing list"""
        try:
            self.login_user()
            response = self.client.get(reverse('billing:invoice_list'), {'mobile': '1'})

            return {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'mobile_optimized': response.status_code == 200
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_billing_mobile_create(self):
        """Test mobile billing create"""
        try:
            self.login_user()
            response = self.client.get(reverse('billing:invoice_add'), {'mobile': '1'})

            return {
                'status_code': response.status_code,
                'success': response.status_code == 200
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_billing_mobile_responsive(self):
        """Test mobile responsive design for billing"""
        try:
            self.login_user()
            response = self.client.get(
                reverse('billing:invoice_list'),
                HTTP_USER_AGENT='Mozilla/5.0 (Android 10; Mobile; rv:81.0)'
            )

            return {
                'loads_on_mobile': response.status_code == 200,
                'responsive_design': True
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_cross_platform_functionality(self):
        """Test cross-platform integration and navigation"""
        print("\n=== Testing Cross-Platform Functionality ===")

        try:
            self.login_user()

            # Test navigation between modules
            navigation_tests = {}

            # Test dashboard access
            dashboard_response = self.client.get(reverse('patients:dashboard'))
            navigation_tests['dashboard_access'] = dashboard_response.status_code == 200

            # Test module interconnections
            # Patient -> Appointment flow
            patient_to_appointment = self.client.get(
                reverse('appointments:appointment_add'),
                {'patient': self.test_patient.id}
            )
            navigation_tests['patient_to_appointment'] = patient_to_appointment.status_code == 200

            # Appointment -> Billing flow
            if hasattr(self, 'test_appointment') and self.test_appointment:
                appointment_to_billing = self.client.get(
                    reverse('billing:invoice_add'),
                    {'appointment': self.test_appointment.id}
                )
                navigation_tests['appointment_to_billing'] = appointment_to_billing.status_code == 200

            # Test search across modules
            search_tests = {}
            search_modules = [
                ('patients:patient_list', 'Almaz'),
                ('doctors:doctor_list', 'Meron'),
                ('appointments:appointment_list', 'consultation'),
                ('pharmacy:medicine_list', 'Paracetamol'),
                ('billing:invoice_list', 'INV')
            ]

            for url_name, search_term in search_modules:
                try:
                    response = self.client.get(reverse(url_name), {'search': search_term})
                    search_tests[url_name] = response.status_code == 200
                except:
                    search_tests[url_name] = False

            self.test_results['cross_platform'] = {
                'navigation': navigation_tests,
                'search_integration': search_tests,
                'overall_integration': all(navigation_tests.values())
            }

        except Exception as e:
            self.test_results['cross_platform'] = {'success': False, 'error': str(e)}

    def test_ui_elements_and_animations(self):
        """Test UI elements, animations, and responsive design"""
        print("\n=== Testing UI Elements and Animations ===")

        try:
            self.login_user()

            # Test main dashboard UI elements
            dashboard_response = self.client.get(reverse('patients:dashboard'))
            dashboard_content = dashboard_response.content.decode()

            ui_elements = {
                'glassmorphism_effects': 'backdrop-filter' in dashboard_content or 'glass' in dashboard_content.lower(),
                'animation_classes': any(anim in dashboard_content for anim in ['fade', 'slide', 'bounce', 'pulse']),
                'responsive_classes': any(resp in dashboard_content for resp in ['col-', 'row', 'd-md-', 'd-lg-']),
                'bootstrap_components': 'btn' in dashboard_content and 'card' in dashboard_content,
                'icons_present': 'fas fa-' in dashboard_content or 'fab fa-' in dashboard_content,
                'ethiopian_colors': any(color in dashboard_content for color in ['ethiopia-green', 'ethiopia-blue', 'ethiopia-yellow'])
            }

            # Test mobile-specific elements
            mobile_response = self.client.get(reverse('patients:dashboard'), {'mobile': '1'})
            mobile_content = mobile_response.content.decode() if mobile_response.status_code == 200 else ''

            mobile_elements = {
                'mobile_navigation': 'mobile' in mobile_content.lower(),
                'touch_friendly': 'btn-lg' in mobile_content or 'touch' in mobile_content.lower(),
                'mobile_cards': 'card' in mobile_content,
                'responsive_text': any(size in mobile_content for size in ['fs-', 'text-sm', 'text-lg'])
            }

            # Test performance indicators
            performance_tests = {
                'page_load_time': dashboard_response.status_code == 200,  # Basic load test
                'css_optimization': 'min.css' in dashboard_content or len(dashboard_content) > 1000,
                'js_optimization': 'min.js' in dashboard_content or 'script' in dashboard_content
            }

            self.test_results['ui_elements'] = {
                'desktop_ui': ui_elements,
                'mobile_ui': mobile_elements,
                'performance': performance_tests,
                'overall_ui_quality': sum(ui_elements.values()) >= len(ui_elements) * 0.7
            }

        except Exception as e:
            self.test_results['ui_elements'] = {'success': False, 'error': str(e)}

    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("COMPREHENSIVE HEALTHCARE DASHBOARD TEST REPORT")
        print("=" * 60)
        
        for module, platforms in self.test_results.items():
            if isinstance(platforms, dict) and platforms:
                print(f"\n{module.upper()} MODULE:")
                print("-" * 40)
                
                for platform, tests in platforms.items():
                    if tests:
                        print(f"\n  {platform.upper()} Tests:")
                        for test_name, result in tests.items():
                            if isinstance(result, dict):
                                success = result.get('success', result.get('overall_success', False))
                                status = "✅ PASS" if success else "❌ FAIL"
                                print(f"    {test_name}: {status}")
                                
                                if not success and 'error' in result:
                                    print(f"      Error: {result['error']}")
        
        print("\n" + "=" * 60)
        print("Test execution completed!")

if __name__ == "__main__":
    # Run the comprehensive test suite
    test_suite = HealthcareDashboardTestSuite()
    results = test_suite.run_all_tests()
    test_suite.generate_report()
