from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.db import models
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.urls import reverse
from .models import Medicine, Prescription
from datetime import datetime, timedelta
from decimal import Decimal

@login_required
def medicine_list_view(request):
    """Medicine list view with search and filtering"""
    medicines = Medicine.objects.all()

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        medicines = medicines.filter(
            Q(name__icontains=search_query) |
            Q(generic_name__icontains=search_query) |
            Q(brand_name__icontains=search_query) |
            Q(manufacturer__icontains=search_query)
        )

    # Filter by category
    category_filter = request.GET.get('category', '')
    if category_filter:
        medicines = medicines.filter(category=category_filter)

    # Filter by form
    form_filter = request.GET.get('form', '')
    if form_filter:
        medicines = medicines.filter(form=form_filter)

    # Filter by stock status
    stock_filter = request.GET.get('stock', '')
    if stock_filter == 'low':
        medicines = medicines.filter(stock_quantity__lte=F('minimum_stock_level'))
    elif stock_filter == 'out':
        medicines = medicines.filter(stock_quantity=0)
    elif stock_filter == 'expired':
        medicines = medicines.filter(expiry_date__lt=datetime.now().date())

    # Pagination
    paginator = Paginator(medicines, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get filter options
    categories = Medicine.objects.values_list('category', flat=True).distinct()
    forms = Medicine.objects.values_list('form', flat=True).distinct()

    # Calculate statistics for mobile stats
    from datetime import datetime, timedelta
    current_month = datetime.now().replace(day=1)
    new_medicines_count = Medicine.objects.filter(created_at__gte=current_month).count()

    # Calculate low stock medicines
    low_stock_count = Medicine.objects.filter(
        is_active=True,
        stock_quantity__lte=F('minimum_stock_level')
    ).count()

    # Calculate expiring soon medicines (within 30 days)
    thirty_days_from_now = timezone.now().date() + timedelta(days=30)
    expiring_soon_count = Medicine.objects.filter(
        is_active=True,
        expiry_date__lte=thirty_days_from_now,
        expiry_date__gte=timezone.now().date()
    ).count()

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'form_filter': form_filter,
        'stock_filter': stock_filter,
        'categories': categories,
        'forms': forms,
        'total_medicines': medicines.count(),
        'new_medicines_count': new_medicines_count,
        'low_stock_count': low_stock_count,
        'expiring_soon_count': expiring_soon_count,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'pharmacy/mobile_list.html' if is_mobile else 'pharmacy/list.html'

    return render(request, template_name, context)

@login_required
def medicine_add_view(request):
    """Add medicine view with form handling"""
    if request.method == 'POST':
        try:
            medicine = Medicine.objects.create(
                name=request.POST.get('name'),
                generic_name=request.POST.get('generic_name', ''),
                brand_name=request.POST.get('brand_name', ''),
                manufacturer=request.POST.get('manufacturer'),
                category=request.POST.get('category'),
                form=request.POST.get('form'),
                strength=request.POST.get('strength'),
                stock_quantity=request.POST.get('stock_quantity', 0),
                minimum_stock_level=request.POST.get('minimum_stock_level', 10),
                unit_price=Decimal(request.POST.get('unit_price', '0')),
                cost_price=Decimal(request.POST.get('cost_price', '0')),
                expiry_date=request.POST.get('expiry_date'),
                description=request.POST.get('description', ''),
                side_effects=request.POST.get('side_effects', ''),
                contraindications=request.POST.get('contraindications', ''),
                storage_instructions=request.POST.get('storage_instructions', ''),
            )

            if request.POST.get('manufacture_date'):
                medicine.manufacture_date = request.POST.get('manufacture_date')
                medicine.save()

            messages.success(request, f'Medicine {medicine.name} added successfully!')
            # Redirect with mobile parameter if it was a mobile request
            if request.GET.get('mobile') == '1' or request.POST.get('mobile') == '1':
                return redirect(f"{reverse('pharmacy:medicine_detail', kwargs={'pk': medicine.pk})}?mobile=1")
            return redirect('pharmacy:medicine_detail', pk=medicine.pk)
        except Exception as e:
            messages.error(request, f'Error adding medicine: {str(e)}')

    context = {
        'categories': Medicine.CATEGORY_CHOICES,
        'forms': Medicine.FORM_CHOICES,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'pharmacy/mobile_add.html' if is_mobile else 'pharmacy/add.html'

    return render(request, template_name, context)

@login_required
def medicine_detail_view(request, pk):
    """Medicine detail view with stock information"""
    medicine = get_object_or_404(Medicine, pk=pk)

    # Get recent prescriptions for this medicine
    prescriptions = Prescription.objects.filter(medicine=medicine).select_related('appointment__patient').order_by('-prescribed_date')[:10]

    context = {
        'medicine': medicine,
        'prescriptions': prescriptions,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'pharmacy/mobile_detail.html' if is_mobile else 'pharmacy/detail.html'

    return render(request, template_name, context)

@login_required
def medicine_edit_view(request, pk):
    """Edit medicine view with form handling"""
    medicine = get_object_or_404(Medicine, pk=pk)

    if request.method == 'POST':
        try:
            medicine.name = request.POST.get('name')
            medicine.generic_name = request.POST.get('generic_name', '')
            medicine.brand_name = request.POST.get('brand_name', '')
            medicine.manufacturer = request.POST.get('manufacturer')
            medicine.category = request.POST.get('category')
            medicine.form = request.POST.get('form')
            medicine.strength = request.POST.get('strength')
            medicine.stock_quantity = request.POST.get('stock_quantity', 0)
            medicine.minimum_stock_level = request.POST.get('minimum_stock_level', 10)
            medicine.unit_price = Decimal(request.POST.get('unit_price', '0'))
            medicine.cost_price = Decimal(request.POST.get('cost_price', '0'))
            medicine.expiry_date = request.POST.get('expiry_date')
            medicine.description = request.POST.get('description', '')
            medicine.side_effects = request.POST.get('side_effects', '')
            medicine.contraindications = request.POST.get('contraindications', '')
            medicine.storage_instructions = request.POST.get('storage_instructions', '')

            if request.POST.get('manufacture_date'):
                medicine.manufacture_date = request.POST.get('manufacture_date')

            medicine.save()

            messages.success(request, f'Medicine {medicine.name} updated successfully!')
            # Redirect with mobile parameter if it was a mobile request
            if request.GET.get('mobile') == '1' or request.POST.get('mobile') == '1':
                return redirect(f"{reverse('pharmacy:medicine_detail', kwargs={'pk': medicine.pk})}?mobile=1")
            return redirect('pharmacy:medicine_detail', pk=medicine.pk)
        except Exception as e:
            messages.error(request, f'Error updating medicine: {str(e)}')

    context = {
        'medicine': medicine,
        'categories': Medicine.CATEGORY_CHOICES,
        'forms': Medicine.FORM_CHOICES,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'pharmacy/mobile_edit.html' if is_mobile else 'pharmacy/edit.html'

    return render(request, template_name, context)

@login_required
def prescription_list_view(request):
    """Prescription list view with filtering"""
    prescriptions = Prescription.objects.select_related('appointment__patient', 'medicine', 'dispensed_by').all()

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        prescriptions = prescriptions.filter(status=status_filter)

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        prescriptions = prescriptions.filter(
            Q(appointment__patient__first_name__icontains=search_query) |
            Q(appointment__patient__last_name__icontains=search_query) |
            Q(medicine__name__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(prescriptions, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate statistics
    all_prescriptions = Prescription.objects.all()
    pending_count = all_prescriptions.filter(status='pending').count()
    dispensed_count = all_prescriptions.filter(status='dispensed').count()
    partially_dispensed_count = all_prescriptions.filter(status='partially_dispensed').count()

    # Count urgent prescriptions (high priority appointments)
    urgent_count = all_prescriptions.filter(
        appointment__priority='urgent',
        status__in=['pending', 'partially_dispensed']
    ).count()

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'statuses': Prescription.STATUS_CHOICES,
        'total_prescriptions': all_prescriptions.count(),
        'pending_count': pending_count,
        'dispensed_count': dispensed_count,
        'partially_dispensed_count': partially_dispensed_count,
        'urgent_count': urgent_count,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'pharmacy/mobile_prescriptions.html' if is_mobile else 'pharmacy/prescriptions.html'

    return render(request, template_name, context)

@login_required
def prescription_dispense_view(request, pk):
    """Dispense prescription view"""
    prescription = get_object_or_404(Prescription.objects.select_related('appointment__patient', 'medicine'), pk=pk)

    if request.method == 'POST':
        try:
            quantity_to_dispense = int(request.POST.get('quantity_dispensed', 0))

            # Validate quantity
            if quantity_to_dispense <= 0:
                messages.error(request, 'Please enter a valid quantity to dispense.')
                return redirect('pharmacy:prescription_dispense', pk=pk)

            remaining_quantity = prescription.remaining_quantity()
            if quantity_to_dispense > remaining_quantity:
                messages.error(request, f'Cannot dispense {quantity_to_dispense} units. Only {remaining_quantity} units remaining.')
                return redirect('pharmacy:prescription_dispense', pk=pk)

            # Check stock availability
            if quantity_to_dispense > prescription.medicine.stock_quantity:
                messages.error(request, f'Insufficient stock. Only {prescription.medicine.stock_quantity} units available.')
                return redirect('pharmacy:prescription_dispense', pk=pk)

            # Update prescription
            prescription.quantity_dispensed += quantity_to_dispense
            if prescription.quantity_dispensed >= prescription.quantity_prescribed:
                prescription.status = 'dispensed'
            else:
                prescription.status = 'partially_dispensed'

            prescription.dispensed_by = request.user
            prescription.dispensed_date = timezone.now()
            prescription.save()

            # Update medicine stock
            prescription.medicine.stock_quantity -= quantity_to_dispense
            prescription.medicine.save()

            messages.success(request, f'Successfully dispensed {quantity_to_dispense} units of {prescription.medicine.name}.')

            # Create notification for successful dispensing
            from notifications.models import Notification
            try:
                Notification.objects.create(
                    title="Prescription Dispensed",
                    message=f"{quantity_to_dispense} units of {prescription.medicine.name} dispensed to {prescription.appointment.patient.get_full_name()}",
                    notification_type='pharmacy',
                    priority='normal',
                    recipient=request.user,
                    action_url=f"/pharmacy/prescriptions/{prescription.pk}/dispense/"
                )
            except:
                pass  # Don't fail if notification creation fails

            # Redirect back to mobile prescriptions if it was a mobile request
            if request.GET.get('mobile') == '1':
                return redirect('pharmacy:prescription_list' + '?mobile=1')
            else:
                return redirect('pharmacy:prescription_list')

        except ValueError as e:
            messages.error(request, f'Invalid quantity entered: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error dispensing prescription: {str(e)}')
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Prescription dispensing error: {str(e)}', exc_info=True)

    context = {
        'prescription': prescription,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'pharmacy/mobile_dispense.html' if is_mobile else 'pharmacy/dispense.html'

    return render(request, template_name, context)


@login_required
def stock_adjustment_view(request, pk):
    """Adjust medicine stock (add/remove stock)"""
    medicine = get_object_or_404(Medicine, pk=pk)

    if request.method == 'POST':
        try:
            adjustment_type = request.POST.get('adjustment_type')  # 'add' or 'remove'
            quantity = int(request.POST.get('quantity', 0))
            reason = request.POST.get('reason', '')

            if quantity <= 0:
                messages.error(request, 'Please enter a valid quantity.')
                # Redirect with mobile parameter if it was a mobile request
                if request.GET.get('mobile') == '1' or request.POST.get('mobile') == '1':
                    return redirect(f"{reverse('pharmacy:stock_adjustment', kwargs={'pk': pk})}?mobile=1")
                return redirect('pharmacy:stock_adjustment', pk=pk)

            old_stock = medicine.stock_quantity

            if adjustment_type == 'add':
                medicine.stock_quantity += quantity
                action = 'added'
            elif adjustment_type == 'remove':
                if quantity > medicine.stock_quantity:
                    messages.error(request, f'Cannot remove {quantity} units. Only {medicine.stock_quantity} units in stock.')
                    # Redirect with mobile parameter if it was a mobile request
                    if request.GET.get('mobile') == '1' or request.POST.get('mobile') == '1':
                        return redirect(f"{reverse('pharmacy:stock_adjustment', kwargs={'pk': pk})}?mobile=1")
                    return redirect('pharmacy:stock_adjustment', pk=pk)
                medicine.stock_quantity -= quantity
                action = 'removed'
            else:
                messages.error(request, 'Invalid adjustment type.')
                # Redirect with mobile parameter if it was a mobile request
                if request.GET.get('mobile') == '1' or request.POST.get('mobile') == '1':
                    return redirect(f"{reverse('pharmacy:stock_adjustment', kwargs={'pk': pk})}?mobile=1")
                return redirect('pharmacy:stock_adjustment', pk=pk)

            medicine.save()

            # Create stock movement record (we'll add this model later)
            messages.success(request, f'Successfully {action} {quantity} units. Stock updated from {old_stock} to {medicine.stock_quantity}.')
            # Redirect with mobile parameter if it was a mobile request
            if request.GET.get('mobile') == '1' or request.POST.get('mobile') == '1':
                return redirect(f"{reverse('pharmacy:medicine_detail', kwargs={'pk': pk})}?mobile=1")
            return redirect('pharmacy:medicine_detail', pk=pk)

        except Exception as e:
            messages.error(request, f'Error adjusting stock: {str(e)}')

    context = {
        'medicine': medicine,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'pharmacy/mobile_stock_adjustment.html' if is_mobile else 'pharmacy/stock_adjustment.html'

    return render(request, template_name, context)


@login_required
def low_stock_report(request):
    """View medicines with low stock"""
    low_stock_medicines = Medicine.objects.filter(
        stock_quantity__lte=F('minimum_stock_level'),
        is_active=True
    ).order_by('stock_quantity')

    # Handle mobile template routing
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'pharmacy/mobile_low_stock_report.html' if is_mobile else 'pharmacy/low_stock_report.html'

    context = {
        'medicines': low_stock_medicines,
        'total_count': low_stock_medicines.count(),
        'today': timezone.now().date(),
    }
    return render(request, template_name, context)


@login_required
def expiring_medicines_report(request):
    """View medicines expiring soon"""
    from datetime import timedelta

    # Medicines expiring in next 30 days
    warning_date = timezone.now().date() + timedelta(days=30)
    next_week = timezone.now().date() + timedelta(days=7)
    expiring_medicines = Medicine.objects.filter(
        expiry_date__lte=warning_date,
        expiry_date__gt=timezone.now().date(),
        is_active=True
    ).order_by('expiry_date')

    # Handle mobile template routing
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'pharmacy/mobile_expiring_report.html' if is_mobile else 'pharmacy/expiring_report.html'

    context = {
        'medicines': expiring_medicines,
        'total_count': expiring_medicines.count(),
        'warning_days': 30,
        'today': timezone.now().date(),
        'next_week': next_week,
    }
    return render(request, template_name, context)


@login_required
def stock_adjustment_ajax_view(request, pk):
    """AJAX endpoint for stock adjustments"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    medicine = get_object_or_404(Medicine, pk=pk)

    try:
        import json
        data = json.loads(request.body)

        adjustment_type = data.get('adjustment_type')
        quantity = int(data.get('quantity', 0))
        reason = data.get('reason', '')
        reference_number = data.get('reference_number', '')
        notes = data.get('notes', '')

        if quantity <= 0:
            return JsonResponse({'success': False, 'message': 'Please enter a valid quantity.'})

        old_stock = medicine.stock_quantity

        if adjustment_type == 'add':
            medicine.stock_quantity += quantity
            action = 'added'
        elif adjustment_type == 'remove':
            if quantity > medicine.stock_quantity:
                return JsonResponse({
                    'success': False,
                    'message': f'Cannot remove {quantity} units. Only {medicine.stock_quantity} units in stock.'
                })
            medicine.stock_quantity -= quantity
            action = 'removed'
        elif adjustment_type == 'set':
            medicine.stock_quantity = quantity
            action = 'set to'
        else:
            return JsonResponse({'success': False, 'message': 'Invalid adjustment type.'})

        medicine.save()

        # Determine stock status
        status = 'low' if medicine.is_low_stock() else 'normal'

        return JsonResponse({
            'success': True,
            'message': f'Successfully {action} {quantity} units. Stock updated from {old_stock} to {medicine.stock_quantity}.',
            'new_stock': medicine.stock_quantity,
            'old_stock': old_stock,
            'status': status,
            'is_low_stock': medicine.is_low_stock()
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error adjusting stock: {str(e)}'})


@login_required
def medicine_stock_info_ajax(request, pk):
    """AJAX endpoint to get current stock information"""
    medicine = get_object_or_404(Medicine, pk=pk)

    return JsonResponse({
        'success': True,
        'current_stock': medicine.stock_quantity,
        'minimum_level': medicine.minimum_stock_level,
        'is_low_stock': medicine.is_low_stock(),
        'is_expired': medicine.is_expired(),
        'is_expiring_soon': medicine.is_expiring_soon(),
        'name': medicine.name,
        'strength': medicine.strength,
        'form': medicine.get_form_display(),
        'category': medicine.get_category_display()
    })


@login_required
def test_stock_functionality_view(request):
    """Test functionality view for debugging pharmacy stock operations"""
    medicines = Medicine.objects.filter(is_active=True).order_by('name')[:10]
    context = {
        'medicines': medicines,
    }
    return render(request, 'pharmacy/test_stock_functionality.html', context)
