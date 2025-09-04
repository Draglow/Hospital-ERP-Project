from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Appointment admin interface"""

    list_display = ('appointment_id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'priority')
    list_filter = ('status', 'priority', 'appointment_type', 'appointment_date', 'doctor__specialty')
    search_fields = ('appointment_id', 'patient__first_name', 'patient__last_name', 'doctor__user__first_name', 'doctor__user__last_name')
    readonly_fields = ('appointment_id', 'created_at', 'updated_at')
    ordering = ('-appointment_date', '-appointment_time')
    date_hierarchy = 'appointment_date'

    fieldsets = (
        ('Appointment Information', {
            'fields': ('appointment_id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'duration_minutes')
        }),
        ('Appointment Details', {
            'fields': ('appointment_type', 'status', 'priority', 'chief_complaint', 'symptoms', 'notes')
        }),
        ('Consultation Details', {
            'fields': ('diagnosis', 'treatment_plan', 'follow_up_required', 'follow_up_date'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('patient', 'doctor__user', 'created_by')
