from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from .models import Appointment
from patients.models import Patient
from doctors.models import Doctor
from datetime import datetime, timedelta, time
import json

@login_required
def appointment_list_view(request):
    """Appointment list view with filtering and search"""
    appointments = Appointment.objects.select_related('patient', 'doctor__user').all()

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        appointments = appointments.filter(
            Q(appointment_id__icontains=search_query) |
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query) |
            Q(doctor__user__first_name__icontains=search_query) |
            Q(doctor__user__last_name__icontains=search_query)
        )

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        appointments = appointments.filter(status=status_filter)

    # Filter by doctor
    doctor_filter = request.GET.get('doctor', '')
    if doctor_filter:
        appointments = appointments.filter(doctor_id=doctor_filter)

    # Filter by date
    date_filter = request.GET.get('date', '')
    if date_filter:
        appointments = appointments.filter(appointment_date=date_filter)

    # Pagination
    paginator = Paginator(appointments, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get filter options
    doctors = Doctor.objects.select_related('user').all()
    statuses = Appointment.STATUS_CHOICES

    # Calculate today's appointments for mobile stats
    today = datetime.now().date()
    today_appointments = Appointment.objects.filter(appointment_date=today).count()

    context = {
        'appointments': page_obj,  # Added for mobile template compatibility
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'doctor_filter': doctor_filter,
        'date_filter': date_filter,
        'doctors': doctors,
        'statuses': statuses,
        'total_appointments': appointments.count(),
        'today_appointments': today_appointments,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'appointments/mobile_list.html' if is_mobile else 'appointments/list.html'

    return render(request, template_name, context)

@login_required
def appointment_add_view(request):
    """Add appointment view with form handling"""
    if request.method == 'POST':
        try:
            # Get patient and doctor
            patient = get_object_or_404(Patient, pk=request.POST.get('patient'))
            doctor = get_object_or_404(Doctor, pk=request.POST.get('doctor'))

            # Create appointment
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=request.POST.get('appointment_date'),
                appointment_time=request.POST.get('appointment_time'),
                appointment_type=request.POST.get('appointment_type'),
                priority=request.POST.get('priority', 'normal'),
                chief_complaint=request.POST.get('chief_complaint'),
                symptoms=request.POST.get('symptoms', ''),
                notes=request.POST.get('notes', ''),
                created_by=request.user,
            )

            messages.success(request, f'Appointment {appointment.appointment_id} created successfully!')
            # Redirect with mobile parameter if it was a mobile request
            if request.GET.get('mobile') == '1' or request.POST.get('mobile') == '1':
                return redirect(f"{reverse('appointments:appointment_detail', kwargs={'pk': appointment.pk})}?mobile=1")
            return redirect('appointments:appointment_detail', pk=appointment.pk)
        except Exception as e:
            messages.error(request, f'Error creating appointment: {str(e)}')

    # Get data for form
    patients = Patient.objects.all()
    doctors = Doctor.objects.select_related('user').all()

    # Pre-select patient if provided in URL
    selected_patient_id = request.GET.get('patient')
    selected_patient = None
    if selected_patient_id:
        try:
            selected_patient = Patient.objects.get(pk=selected_patient_id)
        except Patient.DoesNotExist:
            pass

    context = {
        'patients': patients,
        'doctors': doctors,
        'selected_patient': selected_patient,
        'appointment_types': Appointment.APPOINTMENT_TYPE_CHOICES,
        'priorities': Appointment.PRIORITY_CHOICES,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'appointments/mobile_add.html' if is_mobile else 'appointments/add.html'

    return render(request, template_name, context)

@login_required
def appointment_detail_view(request, pk):
    """Appointment detail view"""
    appointment = get_object_or_404(Appointment.objects.select_related('patient', 'doctor__user', 'created_by'), pk=pk)

    context = {
        'appointment': appointment,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'appointments/mobile_detail.html' if is_mobile else 'appointments/detail.html'

    return render(request, template_name, context)

@login_required
def appointment_edit_view(request, pk):
    """Edit appointment view"""
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        try:
            # Update appointment
            appointment.appointment_date = request.POST.get('appointment_date')
            appointment.appointment_time = request.POST.get('appointment_time')
            appointment.appointment_type = request.POST.get('appointment_type')
            appointment.priority = request.POST.get('priority')
            appointment.status = request.POST.get('status')
            appointment.chief_complaint = request.POST.get('chief_complaint')
            appointment.symptoms = request.POST.get('symptoms', '')
            appointment.notes = request.POST.get('notes', '')
            appointment.diagnosis = request.POST.get('diagnosis', '')
            appointment.treatment_plan = request.POST.get('treatment_plan', '')
            appointment.follow_up_required = 'follow_up_required' in request.POST

            if request.POST.get('follow_up_date'):
                appointment.follow_up_date = request.POST.get('follow_up_date')

            appointment.save()

            messages.success(request, f'Appointment {appointment.appointment_id} updated successfully!')
            # Redirect with mobile parameter if it was a mobile request
            if request.GET.get('mobile') == '1' or request.POST.get('mobile') == '1':
                return redirect(f"{reverse('appointments:appointment_detail', kwargs={'pk': appointment.pk})}?mobile=1")
            return redirect('appointments:appointment_detail', pk=appointment.pk)
        except Exception as e:
            messages.error(request, f'Error updating appointment: {str(e)}')

    context = {
        'appointment': appointment,
        'appointment_types': Appointment.APPOINTMENT_TYPE_CHOICES,
        'priorities': Appointment.PRIORITY_CHOICES,
        'statuses': Appointment.STATUS_CHOICES,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'appointments/mobile_edit.html' if is_mobile else 'appointments/edit.html'

    return render(request, template_name, context)


@login_required
def appointment_cancel_view(request, pk):
    """Cancel appointment view"""
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        if appointment.can_be_cancelled():
            appointment.status = 'cancelled'
            appointment.save()
            messages.success(request, f'Appointment {appointment.appointment_id} has been cancelled.')
        else:
            messages.error(request, 'This appointment cannot be cancelled.')

        # Redirect with mobile parameter if it was a mobile request
        if request.GET.get('mobile') == '1' or request.POST.get('mobile') == '1':
            return redirect(f"{reverse('appointments:appointment_detail', kwargs={'pk': pk})}?mobile=1")
        return redirect('appointments:appointment_detail', pk=pk)

    context = {
        'appointment': appointment,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'appointments/mobile_cancel.html' if is_mobile else 'appointments/cancel.html'

    return render(request, template_name, context)


@login_required
def check_doctor_availability(request):
    """AJAX view to check doctor availability"""
    if request.method == 'GET':
        doctor_id = request.GET.get('doctor_id')
        appointment_date = request.GET.get('appointment_date')
        appointment_time = request.GET.get('appointment_time')
        appointment_id = request.GET.get('appointment_id')  # For editing existing appointments

        if not all([doctor_id, appointment_date, appointment_time]):
            return JsonResponse({'available': False, 'message': 'Missing required parameters'})

        try:
            from datetime import datetime

            # Check if the doctor has another appointment at the same time
            existing_appointments = Appointment.objects.filter(
                doctor_id=doctor_id,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=['scheduled', 'confirmed']
            )

            # Exclude current appointment if editing
            if appointment_id:
                existing_appointments = existing_appointments.exclude(pk=appointment_id)

            if existing_appointments.exists():
                return JsonResponse({
                    'available': False,
                    'message': 'Doctor is not available at this time. Please choose a different time.'
                })

            # Check if the time is in the past
            appointment_datetime = datetime.strptime(f"{appointment_date} {appointment_time}", "%Y-%m-%d %H:%M")
            if appointment_datetime < datetime.now():
                return JsonResponse({
                    'available': False,
                    'message': 'Cannot schedule appointments in the past.'
                })

            return JsonResponse({
                'available': True,
                'message': 'Doctor is available at this time.'
            })

        except Exception as e:
            return JsonResponse({'available': False, 'message': f'Error checking availability: {str(e)}'})

    return JsonResponse({'available': False, 'message': 'Invalid request method'})


@login_required
def appointment_start_view(request, pk):
    """Start appointment - change status from scheduled to in_progress"""
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        try:
            # Validate that appointment can be started
            if appointment.status not in ['scheduled', 'confirmed']:
                return JsonResponse({
                    'success': False,
                    'message': 'This appointment cannot be started. Current status: ' + appointment.get_status_display()
                })

            # Check if appointment is for today or past
            from datetime import datetime
            appointment_datetime = appointment.get_appointment_datetime()
            now = timezone.now()

            if appointment_datetime.date() > now.date():
                return JsonResponse({
                    'success': False,
                    'message': 'Cannot start future appointments. Appointment is scheduled for ' + appointment_datetime.strftime('%B %d, %Y')
                })

            # Update appointment status
            appointment.status = 'in_progress'
            appointment.save()

            return JsonResponse({
                'success': True,
                'message': f'Appointment {appointment.appointment_id} has been started successfully.',
                'new_status': appointment.get_status_display(),
                'status_class': 'warning'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error starting appointment: {str(e)}'
            })

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def appointment_complete_view(request, pk):
    """Complete appointment - change status to completed"""
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        try:
            # Validate that appointment can be completed
            if appointment.status != 'in_progress':
                return JsonResponse({
                    'success': False,
                    'message': 'Only appointments in progress can be completed. Current status: ' + appointment.get_status_display()
                })

            # Update appointment status
            appointment.status = 'completed'
            appointment.save()

            return JsonResponse({
                'success': True,
                'message': f'Appointment {appointment.appointment_id} has been completed successfully.',
                'new_status': appointment.get_status_display(),
                'status_class': 'success'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error completing appointment: {str(e)}'
            })

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def appointment_cancel_ajax_view(request, pk):
    """Cancel appointment via AJAX"""
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        try:
            # Validate that appointment can be cancelled
            if not appointment.can_be_cancelled():
                return JsonResponse({
                    'success': False,
                    'message': 'This appointment cannot be cancelled. It may be in the past or already completed/cancelled.'
                })

            # Update appointment status
            appointment.status = 'cancelled'
            appointment.save()

            return JsonResponse({
                'success': True,
                'message': f'Appointment {appointment.appointment_id} has been cancelled successfully.',
                'new_status': appointment.get_status_display(),
                'status_class': 'danger'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error cancelling appointment: {str(e)}'
            })

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def mobile_test_view(request):
    """Mobile test view for testing appointment actions"""
    return render(request, 'appointments/mobile_test.html')


@login_required
def test_functionality_view(request):
    """Test functionality view for debugging appointment actions"""
    appointments = Appointment.objects.select_related('patient', 'doctor__user').order_by('-created_at')[:10]
    context = {
        'appointments': appointments,
    }
    return render(request, 'appointments/test_functionality.html', context)
