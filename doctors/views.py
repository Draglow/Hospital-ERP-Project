from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.urls import reverse
from .models import Doctor
from accounts.models import User
from appointments.models import Appointment
from datetime import datetime, timedelta

@login_required
def doctor_list_view(request):
    """Doctor list view with search and filtering"""
    doctors = Doctor.objects.select_related('user').all()

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(license_number__icontains=search_query) |
            Q(specialty__icontains=search_query)
        )

    # Filter by specialty
    specialty_filter = request.GET.get('specialty', '')
    if specialty_filter:
        doctors = doctors.filter(specialty=specialty_filter)

    # Filter by availability
    availability_filter = request.GET.get('availability', '')
    if availability_filter:
        doctors = doctors.filter(availability_status=availability_filter)

    # Annotate with appointment counts
    doctors = doctors.annotate(
        total_appointments=Count('appointments'),
        today_appointments=Count('appointments', filter=Q(appointments__appointment_date=datetime.now().date()))
    )

    # Pagination
    paginator = Paginator(doctors, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get filter options
    specialties = Doctor.objects.values_list('specialty', flat=True).distinct()
    availabilities = Doctor.AVAILABILITY_CHOICES

    # Calculate new doctors this month for mobile stats
    current_month = datetime.now().replace(day=1)
    new_doctors_count = Doctor.objects.filter(created_at__gte=current_month).count()

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'specialty_filter': specialty_filter,
        'availability_filter': availability_filter,
        'specialties': specialties,
        'availabilities': availabilities,
        'total_doctors': doctors.count(),
        'new_doctors_count': new_doctors_count,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'doctors/mobile_list.html' if is_mobile else 'doctors/list.html'

    return render(request, template_name, context)

@login_required
def doctor_add_view(request):
    """Add doctor view with form handling"""
    if request.method == 'POST':
        try:
            # Generate unique username
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            base_username = request.POST.get('username', '').strip()

            # If no username provided, generate one
            if not base_username:
                base_username = f"dr.{first_name.lower()}.{last_name.lower()}"

            # Ensure username is unique
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}.{counter}"
                counter += 1

            # Create user first
            user = User.objects.create_user(
                username=username,
                email=request.POST.get('email'),
                first_name=first_name,
                last_name=last_name,
                role='doctor',
                phone=request.POST.get('phone', ''),
                is_staff=True
            )
            user.set_password(request.POST.get('password'))
            user.save()

            # Generate unique license number
            base_license = request.POST.get('license_number', '').strip()

            # If no license number provided, generate one
            if not base_license:
                from datetime import datetime
                year = datetime.now().year
                base_license = f"ETH-MD-{year}-{first_name[:3].upper()}{last_name[:3].upper()}"

            # Ensure license number is unique
            license_number = base_license
            counter = 1
            while Doctor.objects.filter(license_number=license_number).exists():
                if base_license.endswith(f"-{counter-1}") and counter > 1:
                    # Remove previous counter before adding new one
                    base_license = base_license.rsplit(f"-{counter-1}", 1)[0]
                license_number = f"{base_license}-{counter}"
                counter += 1

            # Create doctor profile
            doctor = Doctor.objects.create(
                user=user,
                license_number=license_number,
                specialty=request.POST.get('specialty'),
                sub_specialty=request.POST.get('sub_specialty', ''),
                years_of_experience=request.POST.get('years_of_experience', 0),
                medical_school=request.POST.get('medical_school'),
                graduation_year=request.POST.get('graduation_year'),
                certifications=request.POST.get('certifications', ''),
                consultation_fee=request.POST.get('consultation_fee'),
                availability_status=request.POST.get('availability_status'),
                bio=request.POST.get('bio', ''),
                languages_spoken=request.POST.get('languages_spoken', 'Amharic, English'),
            )

            messages.success(request, f'Doctor {doctor.get_full_name()} added successfully!')
            # Redirect with mobile parameter if it was a mobile request
            if request.GET.get('mobile') == '1' or request.POST.get('mobile') == '1':
                return redirect(f"{reverse('doctors:doctor_detail', kwargs={'pk': doctor.pk})}?mobile=1")
            return redirect('doctors:doctor_detail', pk=doctor.pk)
        except Exception as e:
            messages.error(request, f'Error adding doctor: {str(e)}')

    context = {
        'specialties': Doctor.SPECIALTY_CHOICES,
        'availabilities': Doctor.AVAILABILITY_CHOICES,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'doctors/mobile_add.html' if is_mobile else 'doctors/add.html'

    return render(request, template_name, context)

@login_required
def doctor_detail_view(request, pk):
    """Doctor detail view with appointments and statistics"""
    doctor = get_object_or_404(Doctor.objects.select_related('user'), pk=pk)

    # Get doctor's appointments
    appointments = Appointment.objects.filter(doctor=doctor).select_related('patient').order_by('-appointment_date')

    # Get statistics
    today = datetime.now().date()
    stats = {
        'total_appointments': appointments.count(),
        'today_appointments': appointments.filter(appointment_date=today).count(),
        'completed_appointments': appointments.filter(status='completed').count(),
        'upcoming_appointments': appointments.filter(appointment_date__gte=today, status__in=['scheduled', 'confirmed']).count(),
    }

    context = {
        'doctor': doctor,
        'appointments': appointments[:10],  # Recent 10 appointments
        'stats': stats,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'doctors/mobile_detail.html' if is_mobile else 'doctors/detail.html'

    return render(request, template_name, context)

@login_required
def doctor_edit_view(request, pk):
    """Edit doctor view with form handling"""
    doctor = get_object_or_404(Doctor.objects.select_related('user'), pk=pk)

    if request.method == 'POST':
        try:
            # Update user information
            user = doctor.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.phone = request.POST.get('phone', '')
            user.save()

            # Update doctor information
            doctor.license_number = request.POST.get('license_number')
            doctor.specialty = request.POST.get('specialty')
            doctor.sub_specialty = request.POST.get('sub_specialty', '')
            doctor.years_of_experience = request.POST.get('years_of_experience', 0)
            doctor.medical_school = request.POST.get('medical_school')
            doctor.graduation_year = request.POST.get('graduation_year')
            doctor.certifications = request.POST.get('certifications', '')
            doctor.consultation_fee = request.POST.get('consultation_fee')
            doctor.availability_status = request.POST.get('availability_status')
            doctor.bio = request.POST.get('bio', '')
            doctor.languages_spoken = request.POST.get('languages_spoken', 'Amharic, English')
            doctor.save()

            messages.success(request, f'Doctor {doctor.get_full_name()} updated successfully!')
            # Redirect with mobile parameter if it was a mobile request
            if request.GET.get('mobile') == '1' or request.POST.get('mobile') == '1':
                return redirect(f"{reverse('doctors:doctor_detail', kwargs={'pk': doctor.pk})}?mobile=1")
            return redirect('doctors:doctor_detail', pk=doctor.pk)
        except Exception as e:
            messages.error(request, f'Error updating doctor: {str(e)}')

    context = {
        'doctor': doctor,
        'specialties': Doctor.SPECIALTY_CHOICES,
        'availabilities': Doctor.AVAILABILITY_CHOICES,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'doctors/mobile_edit.html' if is_mobile else 'doctors/edit.html'

    return render(request, template_name, context)

@login_required
def doctor_schedule_view(request, pk):
    """Doctor schedule view with weekly calendar"""
    doctor = get_object_or_404(Doctor.objects.select_related('user'), pk=pk)

    # Get current week appointments
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__range=[week_start, week_end]
    ).select_related('patient').order_by('appointment_date', 'appointment_time')

    # Organize appointments by day
    weekly_schedule = {}
    for i in range(7):
        day = week_start + timedelta(days=i)
        weekly_schedule[day] = appointments.filter(appointment_date=day)

    context = {
        'doctor': doctor,
        'weekly_schedule': weekly_schedule,
        'week_start': week_start,
        'week_end': week_end,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'doctors/mobile_schedule.html' if is_mobile else 'doctors/schedule.html'

    return render(request, template_name, context)
