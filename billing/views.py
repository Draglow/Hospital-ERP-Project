from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from .models import Invoice, InvoiceItem
from patients.models import Patient
from datetime import datetime, timedelta
from decimal import Decimal

@login_required
def invoice_list_view(request):
    """Invoice list view with search and filtering"""
    invoices = Invoice.objects.select_related('patient').all()

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        invoices = invoices.filter(
            Q(invoice_number__icontains=search_query) |
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query) |
            Q(patient__patient_id__icontains=search_query)
        )

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        invoices = invoices.filter(status=status_filter)

    # Filter by payment method
    payment_method_filter = request.GET.get('payment_method', '')
    if payment_method_filter:
        invoices = invoices.filter(payment_method=payment_method_filter)

    # Filter by date range
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    if date_from:
        invoices = invoices.filter(issue_date__gte=date_from)
    if date_to:
        invoices = invoices.filter(issue_date__lte=date_to)

    # Pagination
    paginator = Paginator(invoices, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate totals
    total_amount = invoices.aggregate(total=Sum('total_amount'))['total'] or 0
    paid_amount = invoices.filter(status='paid').aggregate(total=Sum('total_amount'))['total'] or 0
    pending_amount = invoices.filter(status='pending').aggregate(total=Sum('total_amount'))['total'] or 0

    # Calculate new invoices this month for mobile stats
    from datetime import datetime, timedelta
    current_month = datetime.now().replace(day=1)
    new_invoices_count = Invoice.objects.filter(issue_date__gte=current_month).count()

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'payment_method_filter': payment_method_filter,
        'date_from': date_from,
        'date_to': date_to,
        'statuses': Invoice.STATUS_CHOICES,
        'payment_methods': Invoice.PAYMENT_METHOD_CHOICES,
        'total_invoices': invoices.count(),
        'total_amount': total_amount,
        'paid_amount': paid_amount,
        'pending_amount': pending_amount,
        'new_invoices_count': new_invoices_count,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'billing/mobile_list.html' if is_mobile else 'billing/list.html'

    return render(request, template_name, context)

@login_required
def invoice_add_view(request):
    """Add invoice view with form handling"""
    if request.method == 'POST':
        try:
            # Get patient
            patient = get_object_or_404(Patient, pk=request.POST.get('patient'))

            # Create invoice
            invoice = Invoice.objects.create(
                patient=patient,
                issue_date=request.POST.get('issue_date', datetime.now().date()),
                due_date=request.POST.get('due_date'),
                payment_method=request.POST.get('payment_method', 'cash'),
                notes=request.POST.get('notes', ''),
                created_by=request.user,
            )

            # Add invoice items
            item_descriptions = request.POST.getlist('item_description[]')
            item_quantities = request.POST.getlist('item_quantity[]')
            item_prices = request.POST.getlist('item_price[]')

            subtotal = Decimal('0')
            for i, description in enumerate(item_descriptions):
                if description.strip():
                    quantity = int(item_quantities[i]) if i < len(item_quantities) else 1
                    price = Decimal(item_prices[i]) if i < len(item_prices) else Decimal('0')
                    total = quantity * price

                    InvoiceItem.objects.create(
                        invoice=invoice,
                        description=description,
                        quantity=quantity,
                        unit_price=price,
                        total_price=total
                    )
                    subtotal += total

            # Calculate totals
            tax_rate = Decimal(request.POST.get('tax_rate', '15')) / 100  # 15% VAT
            discount_amount = Decimal(request.POST.get('discount_amount', '0'))

            invoice.subtotal = subtotal
            invoice.tax_amount = subtotal * tax_rate
            invoice.discount_amount = discount_amount
            invoice.total_amount = subtotal + invoice.tax_amount - discount_amount
            invoice.save()

            messages.success(request, f'Invoice {invoice.invoice_number} created successfully!')
            # Redirect with mobile parameter if it was a mobile request
            if request.GET.get('mobile') == '1' or request.POST.get('mobile') == '1':
                return redirect(f"{reverse('billing:invoice_detail', kwargs={'pk': invoice.pk})}?mobile=1")
            return redirect('billing:invoice_detail', pk=invoice.pk)
        except Exception as e:
            messages.error(request, f'Error creating invoice: {str(e)}')

    # Get data for form
    patients = Patient.objects.all()

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
        'selected_patient': selected_patient,
        'payment_methods': Invoice.PAYMENT_METHOD_CHOICES,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'billing/mobile_add.html' if is_mobile else 'billing/add.html'

    return render(request, template_name, context)

@login_required
def invoice_detail_view(request, pk):
    """Invoice detail view with items"""
    invoice = get_object_or_404(Invoice.objects.select_related('patient', 'created_by'), pk=pk)
    items = InvoiceItem.objects.filter(invoice=invoice)

    context = {
        'invoice': invoice,
        'items': items,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'billing/mobile_detail.html' if is_mobile else 'billing/detail.html'

    return render(request, template_name, context)

@login_required
def invoice_edit_view(request, pk):
    """Edit invoice view"""
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        try:
            # Update invoice
            invoice.due_date = request.POST.get('due_date')
            invoice.payment_method = request.POST.get('payment_method')
            invoice.notes = request.POST.get('notes', '')
            invoice.status = request.POST.get('status')

            # Update discount
            discount_amount = Decimal(request.POST.get('discount_amount', '0'))
            invoice.discount_amount = discount_amount
            invoice.total_amount = invoice.subtotal + invoice.tax_amount - discount_amount
            invoice.save()

            messages.success(request, f'Invoice {invoice.invoice_number} updated successfully!')
            # Redirect with mobile parameter if it was a mobile request
            if request.GET.get('mobile') == '1' or request.POST.get('mobile') == '1':
                return redirect(f"{reverse('billing:invoice_detail', kwargs={'pk': invoice.pk})}?mobile=1")
            return redirect('billing:invoice_detail', pk=invoice.pk)
        except Exception as e:
            messages.error(request, f'Error updating invoice: {str(e)}')

    context = {
        'invoice': invoice,
        'payment_methods': Invoice.PAYMENT_METHOD_CHOICES,
        'statuses': Invoice.STATUS_CHOICES,
    }

    # Check if mobile version is requested
    is_mobile = request.GET.get('mobile') == '1'
    template_name = 'billing/mobile_edit.html' if is_mobile else 'billing/edit.html'

    return render(request, template_name, context)

@login_required
def invoice_pay_view(request, pk):
    """Process payment for invoice"""
    invoice = get_object_or_404(Invoice.objects.select_related('patient'), pk=pk)

    if request.method == 'POST':
        try:
            payment_amount = Decimal(request.POST.get('payment_amount', '0'))
            payment_method = request.POST.get('payment_method')

            # Update invoice
            invoice.amount_paid += payment_amount
            invoice.payment_method = payment_method
            invoice.payment_date = datetime.now()

            # Update status based on payment
            if invoice.amount_paid >= invoice.total_amount:
                invoice.status = 'paid'
                invoice.balance_due = Decimal('0')
            else:
                invoice.status = 'partially_paid'
                invoice.balance_due = invoice.total_amount - invoice.amount_paid

            invoice.save()

            messages.success(request, f'Payment of {payment_amount} ETB processed successfully!')
            return redirect('billing:invoice_detail', pk=invoice.pk)
        except Exception as e:
            messages.error(request, f'Error processing payment: {str(e)}')

    context = {
        'invoice': invoice,
        'payment_methods': Invoice.PAYMENT_METHOD_CHOICES,
    }
    return render(request, 'billing/pay.html', context)

@login_required
def invoice_pdf_view(request, pk):
    """Generate PDF invoice"""
    invoice = get_object_or_404(Invoice.objects.select_related('patient', 'created_by'), pk=pk)
    items = InvoiceItem.objects.filter(invoice=invoice)

    context = {
        'invoice': invoice,
        'items': items,
    }
    return render(request, 'billing/pdf.html', context)
