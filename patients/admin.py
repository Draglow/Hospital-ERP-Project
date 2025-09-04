from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Patient admin interface"""

    list_display = ('patient_id', 'first_name', 'last_name', 'phone', 'city', 'get_age', 'created_at')
    list_filter = ('gender', 'blood_type', 'city', 'region', 'is_active', 'created_at')
    search_fields = ('patient_id', 'first_name', 'last_name', 'phone', 'email', 'kebele', 'woreda')
    readonly_fields = ('patient_id', 'created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Personal Information', {
            'fields': ('patient_id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'blood_type')
        }),
        ('Address Information', {
            'fields': ('kebele', 'woreda', 'city', 'region')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        ('Medical Information', {
            'fields': ('medical_history', 'allergies', 'current_medications')
        }),
        ('System Information', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_age(self, obj):
        return obj.get_age()
    get_age.short_description = 'Age'
