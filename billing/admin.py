from django.contrib import admin
from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    """Inline admin for invoice items"""
    model = InvoiceItem
    extra = 1
    readonly_fields = ('total_price',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """Invoice admin interface"""

    list_display = ('invoice_number', 'patient', 'doctor', 'total_amount', 'paid_amount', 'status', 'issue_date')
    list_filter = ('status', 'payment_method', 'issue_date', 'due_date')
    search_fields = ('invoice_number', 'patient__first_name', 'patient__last_name', 'doctor__user__first_name')
    readonly_fields = ('invoice_number', 'total_amount', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    date_hierarchy = 'issue_date'
    inlines = [InvoiceItemInline]

    fieldsets = (
        ('Invoice Information', {
            'fields': ('invoice_number', 'patient', 'doctor', 'appointment', 'issue_date', 'due_date', 'status')
        }),
        ('Financial Information', {
            'fields': ('subtotal', 'tax_amount', 'discount_amount', 'total_amount', 'paid_amount')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_date', 'payment_reference'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('patient', 'doctor__user', 'appointment')

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    """Invoice Item admin interface"""

    list_display = ('invoice', 'item_type', 'description', 'quantity', 'unit_price', 'total_price')
    list_filter = ('item_type', 'created_at')
    search_fields = ('invoice__invoice_number', 'description')
    readonly_fields = ('total_price',)
