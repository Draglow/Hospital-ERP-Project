from django.contrib import admin
from django.utils.html import format_html
from .models import Medicine, Prescription

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    """Medicine admin interface"""

    list_display = ('name', 'category', 'form', 'strength', 'stock_quantity', 'unit_price', 'expiry_date', 'stock_status')
    list_filter = ('category', 'form', 'manufacturer', 'is_active', 'expiry_date')
    search_fields = ('name', 'generic_name', 'brand_name', 'manufacturer')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'generic_name', 'brand_name', 'manufacturer', 'category', 'form', 'strength')
        }),
        ('Inventory Information', {
            'fields': ('stock_quantity', 'minimum_stock_level', 'unit_price', 'cost_price')
        }),
        ('Dates', {
            'fields': ('manufacture_date', 'expiry_date')
        }),
        ('Additional Information', {
            'fields': ('description', 'side_effects', 'contraindications', 'storage_instructions'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def stock_status(self, obj):
        if obj.is_expired():
            return format_html('<span style="color: red;">Expired</span>')
        elif obj.is_expiring_soon():
            return format_html('<span style="color: orange;">Expiring Soon</span>')
        elif obj.is_low_stock():
            return format_html('<span style="color: red;">Low Stock</span>')
        else:
            return format_html('<span style="color: green;">Good</span>')
    stock_status.short_description = 'Status'

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    """Prescription admin interface"""

    list_display = ('appointment', 'medicine', 'dosage', 'quantity_prescribed', 'quantity_dispensed', 'status')
    list_filter = ('status', 'prescribed_date', 'medicine__category')
    search_fields = ('appointment__patient__first_name', 'appointment__patient__last_name', 'medicine__name')
    readonly_fields = ('prescribed_date',)
    ordering = ('-prescribed_date',)

    fieldsets = (
        ('Prescription Information', {
            'fields': ('appointment', 'medicine', 'dosage', 'quantity_prescribed', 'duration_days')
        }),
        ('Dispensing Information', {
            'fields': ('quantity_dispensed', 'status', 'dispensed_date', 'dispensed_by')
        }),
        ('Instructions', {
            'fields': ('instructions',)
        }),
        ('System Information', {
            'fields': ('prescribed_date',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('appointment__patient', 'medicine', 'dispensed_by')
