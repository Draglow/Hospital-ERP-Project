from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, F, Count
from django.db import models
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.urls import reverse
from .models import Patient
from appointments.models import Appointment
from billing.models import Invoice
import json
from datetime import datetime, timedelta

@login_required
def dashboard_view(request):
    """Main dashboard view with real statistics and mobile detection"""
    from datetime import timedelta
    from pharmacy.models import Medicine
    from django.shortcuts import redirect

    # Enhanced mobile detection with responsive support
    is_mobile_request = request.GET.get('mobile') == '1'
    force_desktop = request.GET.get('desktop') == '1'
    auto_redirect = request.GET.get('auto_redirect') == '1'

    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    is_mobile_device = any(device in user_agent for device in [
        'mobile', 'android', 'iphone', 'ipad', 'ipod', 'blackberry', 'windows phone'
    ])

    # Redirect mobile devices to mobile dashboard unless explicitly requesting desktop
    # Skip redirect if this was an automatic redirect to prevent loops
    if (is_mobile_device or is_mobile_request) and not force_desktop and not auto_redirect:
        # Preserve query parameters when redirecting
        query_params = request.GET.copy()
        query_params.pop('desktop', None)  # Remove desktop override
        query_params.pop('auto_redirect', None)  # Remove auto redirect flag

        redirect_url = reverse('patients:mobile_dashboard')
        if query_params:
            redirect_url += '?' + query_params.urlencode()

        return redirect(redirect_url)

    # Calculate date ranges first
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    current_month = datetime.now().replace(day=1)
    last_month = (current_month - timedelta(days=1)).replace(day=1)

    # Get real statistics
    total_patients = Patient.objects.count()

    # Doctor statistics
    from doctors.models import Doctor
    total_doctors = Doctor.objects.count()
    current_month_doctors = Doctor.objects.filter(created_at__gte=current_month).count()
    last_month_doctors = Doctor.objects.filter(
        created_at__gte=last_month,
        created_at__lt=current_month
    ).count()
    doctor_change = calculate_percentage_change(last_month_doctors, current_month_doctors)

    # Pharmacy statistics
    total_medicines = Medicine.objects.count()
    current_month_medicines = Medicine.objects.filter(created_at__gte=current_month).count()
    last_month_medicines = Medicine.objects.filter(
        created_at__gte=last_month,
        created_at__lt=current_month
    ).count()
    medicine_change = calculate_percentage_change(last_month_medicines, current_month_medicines)

    # Today's appointments with percentage change
    today_appointments = Appointment.objects.filter(appointment_date=today).count()
    yesterday_appointments = Appointment.objects.filter(appointment_date=yesterday).count()
    appointments_change = calculate_percentage_change(yesterday_appointments, today_appointments)

    # Calculate monthly revenue with percentage change

    monthly_revenue = Invoice.objects.filter(
        issue_date__gte=current_month,
        status='paid'
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    last_month_revenue = Invoice.objects.filter(
        issue_date__gte=last_month,
        issue_date__lt=current_month,
        status='paid'
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    revenue_change = calculate_percentage_change(last_month_revenue, monthly_revenue)

    # Patient growth this month
    current_month_patients = Patient.objects.filter(created_at__gte=current_month).count()
    last_month_patients = Patient.objects.filter(
        created_at__gte=last_month,
        created_at__lt=current_month
    ).count()
    patient_change = calculate_percentage_change(last_month_patients, current_month_patients)

    # Low stock medicines
    low_stock_medicines = Medicine.objects.filter(
        stock_quantity__lte=F('minimum_stock_level'),
        is_active=True
    ).count()

    # Get recent patients
    recent_patients = Patient.objects.order_by('-created_at')[:5]

    # Get recent appointments
    recent_appointments = Appointment.objects.select_related('patient', 'doctor__user').order_by('-created_at')[:5]

    # Get recent doctors
    recent_doctors = Doctor.objects.select_related('user').order_by('-created_at')[:5]

    # Get recent medicines
    recent_medicines = Medicine.objects.order_by('-created_at')[:5]

    # Get patient trends data for chart (last 6 months)
    patient_trends = get_patient_trends_data()

    # Get patient demographics data
    patient_demographics = get_patient_demographics_data()

    # Get appointments by doctor data
    appointments_by_doctor = get_appointments_by_doctor_data()

    # Get revenue breakdown data
    revenue_breakdown = get_revenue_breakdown_data()

    # Get recent activity
    recent_activity = get_recent_activity()

    context = {
        'total_patients': total_patients,
        'today_appointments': today_appointments,
        'monthly_revenue': monthly_revenue,
        'low_stock_medicines': low_stock_medicines,
        'appointments_change': appointments_change,
        'revenue_change': revenue_change,
        'patient_change': patient_change,
        'total_doctors': total_doctors,
        'doctor_change': doctor_change,
        'total_medicines': total_medicines,
        'medicine_change': medicine_change,
        'recent_patients': recent_patients,
        'recent_appointments': recent_appointments,
        'recent_doctors': recent_doctors,
        'recent_medicines': recent_medicines,
        'patient_trends': patient_trends,
        'patient_demographics': patient_demographics,
        'appointments_by_doctor': appointments_by_doctor,
        'revenue_breakdown': revenue_breakdown,
        'recent_activity': recent_activity,
        'is_mobile_device': is_mobile_device,
        'is_mobile_request': is_mobile_request,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def mobile_dashboard_view(request):
    """Mobile dashboard view with same data as desktop but mobile template"""
    from datetime import timedelta
    from pharmacy.models import Medicine

    # Enhanced responsive detection
    force_mobile = request.GET.get('mobile') == '1'
    force_desktop = request.GET.get('desktop') == '1'
    auto_redirect = request.GET.get('auto_redirect') == '1'

    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    is_mobile_device = any(device in user_agent for device in [
        'mobile', 'android', 'iphone', 'ipad', 'ipod', 'blackberry', 'windows phone'
    ])

    # Redirect to desktop if explicitly requested and not an auto redirect
    if force_desktop and not auto_redirect:
        # Preserve query parameters when redirecting
        query_params = request.GET.copy()
        query_params.pop('mobile', None)  # Remove mobile override
        query_params.pop('auto_redirect', None)  # Remove auto redirect flag

        redirect_url = reverse('patients:dashboard')
        if query_params:
            redirect_url += '?' + query_params.urlencode()

        return redirect(redirect_url)

    # Calculate date ranges first
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    current_month = datetime.now().replace(day=1)
    last_month = (current_month - timedelta(days=1)).replace(day=1)

    # Get real statistics (same as desktop dashboard)
    total_patients = Patient.objects.count()

    # Doctor statistics
    from doctors.models import Doctor
    total_doctors = Doctor.objects.count()
    current_month_doctors = Doctor.objects.filter(created_at__gte=current_month).count()
    last_month_doctors = Doctor.objects.filter(
        created_at__gte=last_month,
        created_at__lt=current_month
    ).count()
    doctor_change = calculate_percentage_change(last_month_doctors, current_month_doctors)

    # Pharmacy statistics
    total_medicines = Medicine.objects.count()
    current_month_medicines = Medicine.objects.filter(created_at__gte=current_month).count()
    last_month_medicines = Medicine.objects.filter(
        created_at__gte=last_month,
        created_at__lt=current_month
    ).count()
    medicine_change = calculate_percentage_change(last_month_medicines, current_month_medicines)

    # Today's appointments with percentage change
    today_appointments = Appointment.objects.filter(appointment_date=today).count()
    yesterday_appointments = Appointment.objects.filter(appointment_date=yesterday).count()
    appointments_change = calculate_percentage_change(yesterday_appointments, today_appointments)

    # Calculate monthly revenue with percentage change

    monthly_revenue = Invoice.objects.filter(
        issue_date__gte=current_month,
        status='paid'
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    last_month_revenue = Invoice.objects.filter(
        issue_date__gte=last_month,
        issue_date__lt=current_month,
        status='paid'
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    revenue_change = calculate_percentage_change(last_month_revenue, monthly_revenue)

    # Patient growth this month
    current_month_patients = Patient.objects.filter(created_at__gte=current_month).count()
    last_month_patients = Patient.objects.filter(
        created_at__gte=last_month,
        created_at__lt=current_month
    ).count()
    patient_change = calculate_percentage_change(last_month_patients, current_month_patients)

    # Low stock medicines
    low_stock_medicines = Medicine.objects.filter(
        stock_quantity__lte=F('minimum_stock_level'),
        is_active=True
    ).count()

    # Get recent patients
    recent_patients = Patient.objects.order_by('-created_at')[:5]

    # Get recent appointments
    recent_appointments = Appointment.objects.select_related('patient', 'doctor__user').order_by('-created_at')[:5]

    # Get recent doctors
    recent_doctors = Doctor.objects.select_related('user').order_by('-created_at')[:5]

    # Get recent medicines
    recent_medicines = Medicine.objects.order_by('-created_at')[:5]

    # Get patient trends data for chart (last 6 months)
    patient_trends = get_patient_trends_data()

    # Get patient demographics data
    patient_demographics = get_patient_demographics_data()

    # Get appointments by doctor data
    appointments_by_doctor = get_appointments_by_doctor_data()

    # Get revenue breakdown data
    revenue_breakdown = get_revenue_breakdown_data()

    # Get recent activity
    recent_activity = get_recent_activity()

    # Additional statistics for the new mobile layout
    # Total appointments this month
    total_appointments_month = Appointment.objects.filter(
        appointment_date__gte=current_month
    ).count()
    last_month_appointments = Appointment.objects.filter(
        appointment_date__gte=last_month,
        appointment_date__lt=current_month
    ).count()
    total_appointments_change = calculate_percentage_change(last_month_appointments, total_appointments_month)

    # New patients this month (already calculated above as current_month_patients)
    new_patients_month = current_month_patients
    new_patients_change = calculate_percentage_change(last_month_patients, new_patients_month)

    # New doctors this month (already calculated above as current_month_doctors)
    new_doctors_month = current_month_doctors
    new_doctors_change = calculate_percentage_change(last_month_doctors, new_doctors_month)

    # Yearly revenue
    current_year = datetime.now().year
    yearly_revenue = Invoice.objects.filter(
        issue_date__year=current_year,
        status='paid'
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    last_year_revenue = Invoice.objects.filter(
        issue_date__year=current_year - 1,
        status='paid'
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    yearly_revenue_change = calculate_percentage_change(last_year_revenue, yearly_revenue)

    context = {
        'total_patients': total_patients,
        'today_appointments': today_appointments,
        'monthly_revenue': monthly_revenue,
        'low_stock_medicines': low_stock_medicines,
        'appointments_change': appointments_change,
        'revenue_change': revenue_change,
        'patient_change': patient_change,
        'total_doctors': total_doctors,
        'doctor_change': doctor_change,
        'total_medicines': total_medicines,
        'medicine_change': medicine_change,
        'recent_patients': recent_patients,
        'recent_appointments': recent_appointments,
        'recent_doctors': recent_doctors,
        'recent_medicines': recent_medicines,
        'patient_trends': patient_trends,
        'patient_demographics': patient_demographics,
        'appointments_by_doctor': appointments_by_doctor,
        'revenue_breakdown': revenue_breakdown,
        'recent_activity': recent_activity,
        # Additional context for new mobile layout
        'total_appointments_month': total_appointments_month,
        'total_appointments_change': total_appointments_change,
        'new_patients_month': new_patients_month,
        'new_patients_change': new_patients_change,
        'new_doctors_month': new_doctors_month,
        'new_doctors_change': new_doctors_change,
        'yearly_revenue': yearly_revenue,
        'yearly_revenue_change': yearly_revenue_change,
    }
    return render(request, 'dashboard/mobile/index.html', context)


@login_required
def responsive_detection_test_view(request):
    """Responsive detection test view for testing automatic dashboard switching"""
    return render(request, 'dashboard/responsive-detection-test.html')


@login_required
def mobile_responsive_test_view(request):
    """Mobile responsive test view for testing mobile dashboard features"""
    return render(request, 'dashboard/mobile/responsive-test.html')


def calculate_percentage_change(old_value, new_value):
    """Calculate percentage change between two values"""
    if old_value == 0:
        return {'percentage': 100 if new_value > 0 else 0, 'direction': 'up' if new_value > 0 else 'neutral'}

    change = ((new_value - old_value) / old_value) * 100
    return {
        'percentage': abs(round(change, 1)),
        'direction': 'up' if change > 0 else 'down' if change < 0 else 'neutral'
    }


def get_patient_trends_data():
    """Get enhanced patient registration trends for the last 6 months"""
    from django.db.models.functions import TruncMonth, TruncWeek
    from datetime import datetime, timedelta

    six_months_ago = datetime.now() - timedelta(days=180)

    # Monthly trends
    monthly_trends = Patient.objects.filter(
        created_at__gte=six_months_ago
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    # Format data for chart
    labels = []
    data = []

    # Ensure we have data for all 6 months
    current_date = datetime.now()
    for i in range(6):
        month_date = current_date.replace(day=1) - timedelta(days=30*i)
        month_label = month_date.strftime('%b %Y')

        # Find matching data
        month_count = 0
        for trend in monthly_trends:
            if trend['month'].strftime('%b %Y') == month_label:
                month_count = trend['count']
                break

        labels.insert(0, month_label)
        data.insert(0, month_count)

    return {
        'labels': labels,
        'data': data,
        'total_new_patients': sum(data),
        'average_per_month': round(sum(data) / len(data), 1) if data else 0
    }


def get_patient_demographics_data():
    """Get patient demographics breakdown"""
    total_patients = Patient.objects.count()

    # Gender distribution
    gender_data = Patient.objects.values('gender').annotate(
        count=Count('id')
    ).order_by('gender')

    # Age groups
    from django.utils import timezone
    today = timezone.now().date()

    age_groups = {
        '0-18': 0,
        '19-35': 0,
        '36-50': 0,
        '51-65': 0,
        '65+': 0
    }

    for patient in Patient.objects.all():
        age = (today - patient.date_of_birth).days // 365
        if age <= 18:
            age_groups['0-18'] += 1
        elif age <= 35:
            age_groups['19-35'] += 1
        elif age <= 50:
            age_groups['36-50'] += 1
        elif age <= 65:
            age_groups['51-65'] += 1
        else:
            age_groups['65+'] += 1

    return {
        'gender_distribution': {
            'labels': [dict(Patient.GENDER_CHOICES).get(item['gender'], item['gender']) for item in gender_data],
            'data': [item['count'] for item in gender_data]
        },
        'age_distribution': {
            'labels': list(age_groups.keys()),
            'data': list(age_groups.values())
        },
        'total_patients': total_patients
    }


def get_appointments_by_doctor_data():
    """Get enhanced appointments analytics by doctor for current month"""
    current_month = datetime.now().replace(day=1)

    # Get appointment counts and completion rates by doctor
    from django.db.models import Case, When, IntegerField

    doctor_stats = Appointment.objects.filter(
        appointment_date__gte=current_month
    ).values(
        'doctor__user__first_name',
        'doctor__user__last_name',
        'doctor__id'
    ).annotate(
        total_appointments=Count('id'),
        completed_appointments=Count(
            Case(
                When(status='completed', then=1),
                output_field=IntegerField()
            )
        ),
        cancelled_appointments=Count(
            Case(
                When(status='cancelled', then=1),
                output_field=IntegerField()
            )
        )
    ).order_by('-total_appointments')[:5]

    labels = []
    data = []
    completion_rates = []

    for stats in doctor_stats:
        doctor_name = f"Dr. {stats['doctor__user__first_name']} {stats['doctor__user__last_name']}"
        labels.append(doctor_name)
        data.append(stats['total_appointments'])

        # Calculate completion rate
        if stats['total_appointments'] > 0:
            completion_rate = (stats['completed_appointments'] / stats['total_appointments']) * 100
        else:
            completion_rate = 0
        completion_rates.append(round(completion_rate, 1))

    # Create combined data for template iteration
    doctor_performance = []
    for i, label in enumerate(labels):
        doctor_performance.append({
            'name': label,
            'appointments': data[i] if i < len(data) else 0,
            'completion_rate': completion_rates[i] if i < len(completion_rates) else 0
        })

    return {
        'labels': labels,
        'data': data,
        'completion_rates': completion_rates,
        'doctor_performance': doctor_performance,
        'total_appointments_this_month': sum(data)
    }


def get_revenue_breakdown_data():
    """Get revenue breakdown by appointment type for current month"""
    current_month = datetime.now().replace(day=1)

    # Get revenue by appointment type from invoices
    revenue_data = Invoice.objects.filter(
        issue_date__gte=current_month,
        status='paid',
        appointment__isnull=False
    ).values(
        'appointment__appointment_type'
    ).annotate(
        total_revenue=Sum('total_amount')
    ).order_by('-total_revenue')

    # Get pharmacy revenue (invoices without appointments)
    pharmacy_revenue = Invoice.objects.filter(
        issue_date__gte=current_month,
        status='paid',
        appointment__isnull=True
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    labels = []
    data = []

    # Map appointment types to readable names
    type_mapping = {
        'consultation': 'Consultations',
        'follow_up': 'Follow-ups',
        'emergency': 'Emergency',
        'surgery': 'Surgery',
        'checkup': 'Checkups',
        'vaccination': 'Vaccinations',
        'lab_test': 'Lab Tests',
    }

    for item in revenue_data:
        appointment_type = item['appointment__appointment_type']
        readable_name = type_mapping.get(appointment_type, appointment_type.title())
        labels.append(readable_name)
        data.append(float(item['total_revenue']))

    # Add pharmacy revenue if exists
    if pharmacy_revenue > 0:
        labels.append('Pharmacy')
        data.append(float(pharmacy_revenue))

    return {'labels': labels, 'data': data}


def get_recent_activity():
    """Get recent system activity"""
    activities = []

    # Recent patient registrations
    recent_patients = Patient.objects.order_by('-created_at')[:3]
    for patient in recent_patients:
        activities.append({
            'icon': 'fas fa-user-plus',
            'color': 'success',
            'title': 'New patient registered',
            'description': f"{patient.get_full_name()} - {patient.created_at}",
            'time': patient.created_at
        })

    # Recent appointments
    recent_appointments = Appointment.objects.order_by('-created_at')[:3]
    for appointment in recent_appointments:
        activities.append({
            'icon': 'fas fa-calendar-plus',
            'color': 'primary',
            'title': 'New appointment scheduled',
            'description': f"{appointment.patient.get_full_name()} with {appointment.doctor.get_full_name()} - {appointment.created_at}",
            'time': appointment.created_at
        })

    # Recent invoices
    from billing.models import Invoice
    recent_invoices = Invoice.objects.order_by('-created_at')[:2]
    for invoice in recent_invoices:
        activities.append({
            'icon': 'fas fa-file-invoice',
            'color': 'warning',
            'title': 'Invoice created',
            'description': f"Invoice {invoice.invoice_number} for {invoice.patient.get_full_name()} - {invoice.created_at}",
            'time': invoice.created_at
        })

    # Sort by time and return latest 8
    activities.sort(key=lambda x: x['time'], reverse=True)
    return activities[:8]


@login_required
def dashboard_stats_api(request):
    """API endpoint for real-time dashboard statistics"""
    from django.http import JsonResponse
    from pharmacy.models import Medicine

    try:
        # Get real statistics
        total_patients = Patient.objects.count()
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        # Today's appointments
        today_appointments = Appointment.objects.filter(appointment_date=today).count()

        # Calculate monthly revenue
        current_month = datetime.now().replace(day=1)
        monthly_revenue = Invoice.objects.filter(
            issue_date__gte=current_month,
            status='paid'
        ).aggregate(total=Sum('total_amount'))['total'] or 0

        # Low stock medicines
        low_stock_medicines = Medicine.objects.filter(
            stock_quantity__lte=F('minimum_stock_level'),
            is_active=True
        ).count()

        # Doctor statistics
        from doctors.models import Doctor
        total_doctors = Doctor.objects.count()

        # Medicine statistics
        total_medicines = Medicine.objects.count()

        # Additional statistics for mobile dashboard
        # Total appointments this month
        total_appointments_month = Appointment.objects.filter(
            appointment_date__gte=current_month
        ).count()

        # New patients this month
        new_patients_month = Patient.objects.filter(created_at__gte=current_month).count()

        # New doctors this month
        new_doctors_month = Doctor.objects.filter(created_at__gte=current_month).count()

        # Yearly revenue
        current_year = datetime.now().year
        yearly_revenue = Invoice.objects.filter(
            issue_date__year=current_year,
            status='paid'
        ).aggregate(total=Sum('total_amount'))['total'] or 0

        return JsonResponse({
            'success': True,
            'total_patients': total_patients,
            'today_appointments': today_appointments,
            'monthly_revenue': float(monthly_revenue),
            'low_stock_medicines': low_stock_medicines,
            'total_doctors': total_doctors,
            'total_medicines': total_medicines,
            'total_appointments_month': total_appointments_month,
            'new_patients_month': new_patients_month,
            'new_doctors_month': new_doctors_month,
            'yearly_revenue': float(yearly_revenue),
            'timestamp': timezone.now().isoformat()
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def patient_list_view(request):
    """Patient list view with search and filtering"""
    patients = Patient.objects.all()

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        patients = patients.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(patient_id__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # Filter by gender
    gender_filter = request.GET.get('gender', '')
    if gender_filter:
        patients = patients.filter(gender=gender_filter)

    # Filter by city
    city_filter = request.GET.get('city', '')
    if city_filter:
        patients = patients.filter(city=city_filter)

    # Filter by blood type
    blood_type_filter = request.GET.get('blood_type', '')
    if blood_type_filter:
        patients = patients.filter(blood_type=blood_type_filter)

    # Pagination
    paginator = Paginator(patients, 10)  # Show 10 patients per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get filter options
    cities = Patient.objects.values_list('city', flat=True).distinct()
    blood_types = Patient.objects.values_list('blood_type', flat=True).distinct()

    # Calculate new patients this month for mobile stats
    from datetime import datetime, timedelta
    current_month = datetime.now().replace(day=1)
    new_patients_count = Patient.objects.filter(created_at__gte=current_month).count()

    context = {
        'patients': page_obj,  # Changed to 'patients' for mobile template compatibility
        'page_obj': page_obj,
        'search_query': search_query,
        'gender_filter': gender_filter,
        'city_filter': city_filter,
        'blood_type_filter': blood_type_filter,
        'cities': cities,
        'blood_types': blood_types,
        'total_patients': patients.count(),
        'new_patients_count': new_patients_count,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'patients/mobile_list.html' if is_mobile else 'patients/list.html'

    return render(request, template_name, context)

@login_required
def patient_add_view(request):
    """Add patient view with form handling"""
    if request.method == 'POST':
        try:
            # Create new patient
            patient = Patient.objects.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                date_of_birth=request.POST.get('date_of_birth'),
                gender=request.POST.get('gender'),
                blood_type=request.POST.get('blood_type', ''),
                kebele=request.POST.get('kebele'),
                woreda=request.POST.get('woreda'),
                city=request.POST.get('city'),
                region=request.POST.get('region'),
                phone=request.POST.get('phone'),
                email=request.POST.get('email', ''),
                emergency_contact_name=request.POST.get('emergency_contact_name'),
                emergency_contact_phone=request.POST.get('emergency_contact_phone'),
                emergency_contact_relationship=request.POST.get('emergency_contact_relationship'),
                medical_history=request.POST.get('medical_history', ''),
                allergies=request.POST.get('allergies', ''),
                current_medications=request.POST.get('current_medications', ''),
            )
            messages.success(request, f'Patient {patient.get_full_name()} added successfully!')
            # Redirect with mobile parameter if it was a mobile request
            if request.GET.get('mobile') == '1' or request.POST.get('mobile') == '1':
                return redirect(f"{reverse('patients:patient_detail', kwargs={'pk': patient.pk})}?mobile=1")
            return redirect('patients:patient_detail', pk=patient.pk)
        except Exception as e:
            messages.error(request, f'Error adding patient: {str(e)}')

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'patients/mobile_add.html' if is_mobile else 'patients/add.html'

    return render(request, template_name)

@login_required
def patient_detail_view(request, pk):
    """Patient detail view with complete information"""
    patient = get_object_or_404(Patient, pk=pk)

    # Get patient's appointments
    appointments = Appointment.objects.filter(patient=patient).select_related('doctor__user').order_by('-appointment_date')

    # Get patient's invoices
    invoices = Invoice.objects.filter(patient=patient).order_by('-created_at')

    context = {
        'patient': patient,
        'appointments': appointments,
        'invoices': invoices,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'patients/mobile_detail.html' if is_mobile else 'patients/detail.html'

    return render(request, template_name, context)

@login_required
def patient_edit_view(request, pk):
    """Edit patient view with form handling"""
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        try:
            # Update patient information
            patient.first_name = request.POST.get('first_name')
            patient.last_name = request.POST.get('last_name')
            patient.date_of_birth = request.POST.get('date_of_birth')
            patient.gender = request.POST.get('gender')
            patient.blood_type = request.POST.get('blood_type', '')
            patient.kebele = request.POST.get('kebele')
            patient.woreda = request.POST.get('woreda')
            patient.city = request.POST.get('city')
            patient.region = request.POST.get('region')
            patient.phone = request.POST.get('phone')
            patient.email = request.POST.get('email', '')
            patient.emergency_contact_name = request.POST.get('emergency_contact_name')
            patient.emergency_contact_phone = request.POST.get('emergency_contact_phone')
            patient.emergency_contact_relationship = request.POST.get('emergency_contact_relationship')
            patient.medical_history = request.POST.get('medical_history', '')
            patient.allergies = request.POST.get('allergies', '')
            patient.current_medications = request.POST.get('current_medications', '')
            patient.save()

            messages.success(request, f'Patient {patient.get_full_name()} updated successfully!')
            # Redirect with mobile parameter if it was a mobile request
            if request.GET.get('mobile') == '1' or request.POST.get('mobile') == '1':
                return redirect(f"{reverse('patients:patient_detail', kwargs={'pk': patient.pk})}?mobile=1")
            return redirect('patients:patient_detail', pk=patient.pk)
        except Exception as e:
            messages.error(request, f'Error updating patient: {str(e)}')

    context = {
        'patient': patient,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'patients/mobile_edit.html' if is_mobile else 'patients/edit.html'

    return render(request, template_name, context)

@login_required
def patient_delete_view(request, pk):
    """Delete patient view"""
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        patient_name = patient.get_full_name()
        patient.delete()
        messages.success(request, f'Patient {patient_name} deleted successfully!')

        # Redirect with mobile parameter if it was a mobile request
        if request.GET.get('mobile') == '1' or request.POST.get('mobile') == '1':
            return redirect('patients:patient_list?mobile=1')
        return redirect('patients:patient_list')

    context = {
        'patient': patient,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'patients/mobile_delete.html' if is_mobile else 'patients/delete.html'

    return render(request, template_name, context)

@login_required
def patient_export_view(request):
    """Export patients to CSV"""
    import csv
    from django.http import HttpResponse

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patients.csv"'

    writer = csv.writer(response)
    writer.writerow(['Patient ID', 'Name', 'Age', 'Gender', 'Phone', 'City', 'Blood Type', 'Created Date'])

    patients = Patient.objects.all()
    for patient in patients:
        writer.writerow([
            patient.patient_id,
            patient.get_full_name(),
            patient.get_age(),
            patient.get_gender_display(),
            patient.phone,
            patient.city,
            patient.blood_type,
            patient.created_at.strftime('%Y-%m-%d')
        ])

    return response

@login_required
def patient_search_ajax(request):
    """AJAX search for patients"""
    query = request.GET.get('q', '')
    patients = []

    if query:
        patient_objects = Patient.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(patient_id__icontains=query)
        )[:10]

        patients = [{
            'id': patient.id,
            'patient_id': patient.patient_id,
            'name': patient.get_full_name(),
            'phone': patient.phone,
            'city': patient.city,
        } for patient in patient_objects]

    return JsonResponse({'patients': patients})


@login_required
def global_search_ajax(request):
    """Global AJAX search across all modules"""
    query = request.GET.get('q', '')
    results = []

    if query and len(query) >= 2:
        # Search patients
        patients = Patient.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(patient_id__icontains=query)
        )[:5]

        for patient in patients:
            results.append({
                'type': 'patient',
                'id': patient.id,
                'title': patient.get_full_name(),
                'subtitle': f"ID: {patient.patient_id}",
                'url': f"/dashboard/patients/{patient.id}/",
                'icon': 'user'
            })

        # Search appointments
        from appointments.models import Appointment
        appointments = Appointment.objects.select_related('patient', 'doctor__user').filter(
            Q(appointment_id__icontains=query) |
            Q(patient__first_name__icontains=query) |
            Q(patient__last_name__icontains=query) |
            Q(doctor__user__first_name__icontains=query) |
            Q(doctor__user__last_name__icontains=query)
        )[:5]

        for appointment in appointments:
            results.append({
                'type': 'appointment',
                'id': appointment.id,
                'title': f"{appointment.patient.get_full_name()} - {appointment.doctor.user.get_full_name()}",
                'subtitle': f"ID: {appointment.appointment_id} | {appointment.appointment_date}",
                'url': f"/appointments/{appointment.id}/",
                'icon': 'calendar-alt'
            })

        # Search doctors
        from doctors.models import Doctor
        doctors = Doctor.objects.select_related('user').filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(license_number__icontains=query) |
            Q(specialty__icontains=query)
        )[:5]

        for doctor in doctors:
            results.append({
                'type': 'doctor',
                'id': doctor.id,
                'title': doctor.user.get_full_name(),
                'subtitle': f"Specialty: {doctor.specialty}",
                'url': f"/doctors/{doctor.id}/",
                'icon': 'user-md'
            })

        # Search medicines
        from pharmacy.models import Medicine
        medicines = Medicine.objects.filter(
            Q(name__icontains=query) |
            Q(generic_name__icontains=query) |
            Q(brand_name__icontains=query)
        )[:5]

        for medicine in medicines:
            results.append({
                'type': 'medicine',
                'id': medicine.id,
                'title': medicine.name,
                'subtitle': f"Generic: {medicine.generic_name}",
                'url': f"/pharmacy/medicines/{medicine.id}/",
                'icon': 'pills'
            })

    return JsonResponse({'results': results})


@login_required
def mobile_navigation_test_view(request):
    """Mobile navigation test view to verify all links work correctly"""
    context = {
        'test_results': [],
        'navigation_links': [
            {'name': 'Dashboard', 'url': 'patients:mobile_dashboard', 'params': ''},
            {'name': 'Patients', 'url': 'patients:patient_list', 'params': '?mobile=1'},
            {'name': 'Appointments', 'url': 'appointments:appointment_list', 'params': '?mobile=1'},
            {'name': 'Doctors', 'url': 'doctors:doctor_list', 'params': '?mobile=1'},
            {'name': 'Billing', 'url': 'billing:invoice_list', 'params': '?mobile=1'},
            {'name': 'Pharmacy', 'url': 'pharmacy:medicine_list', 'params': '?mobile=1'},
            {'name': 'Profile', 'url': 'accounts:profile', 'params': '?mobile=1'},
            {'name': 'Settings', 'url': 'accounts:settings', 'params': '?mobile=1'},
        ]
    }
    return render(request, 'dashboard/mobile/navigation-test.html', context)

@login_required
def mobile_crud_test_view(request):
    """Mobile CRUD testing view for comprehensive testing of all operations"""
    context = {
        'modules': [
            {
                'name': 'patients',
                'title': 'Patient Management',
                'description': 'Test patient CRUD operations',
                'icon': 'fas fa-users',
                'color': 'primary',
                'list_url': 'patients:patient_list',
                'add_url': 'patients:patient_add',
            },
            {
                'name': 'appointments',
                'title': 'Appointment Management',
                'description': 'Test appointment CRUD operations',
                'icon': 'fas fa-calendar-alt',
                'color': 'success',
                'list_url': 'appointments:appointment_list',
                'add_url': 'appointments:appointment_add',
            },
            {
                'name': 'doctors',
                'title': 'Doctor Management',
                'description': 'Test doctor CRUD operations',
                'icon': 'fas fa-user-md',
                'color': 'info',
                'list_url': 'doctors:doctor_list',
                'add_url': 'doctors:doctor_add',
            },
            {
                'name': 'billing',
                'title': 'Billing Management',
                'description': 'Test billing CRUD operations',
                'icon': 'fas fa-file-invoice-dollar',
                'color': 'warning',
                'list_url': 'billing:invoice_list',
                'add_url': 'billing:invoice_add',
            },
            {
                'name': 'pharmacy',
                'title': 'Pharmacy Management',
                'description': 'Test pharmacy CRUD operations',
                'icon': 'fas fa-pills',
                'color': 'ethiopia-green',
                'list_url': 'pharmacy:medicine_list',
                'add_url': 'pharmacy:medicine_add',
            }
        ]
    }

    return render(request, 'patients/mobile_crud_test.html', context)
