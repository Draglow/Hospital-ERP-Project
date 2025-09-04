from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """Doctor admin interface"""

    list_display = ('get_full_name', 'specialty', 'license_number', 'consultation_fee', 'availability_status', 'is_active')
    list_filter = ('specialty', 'availability_status', 'is_active', 'graduation_year')
    search_fields = ('user__first_name', 'user__last_name', 'license_number', 'medical_school')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('user__first_name', 'user__last_name')

    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Professional Information', {
            'fields': ('license_number', 'specialty', 'sub_specialty', 'years_of_experience')
        }),
        ('Education', {
            'fields': ('medical_school', 'graduation_year', 'certifications')
        }),
        ('Practice Information', {
            'fields': ('consultation_fee', 'availability_status', 'bio', 'languages_spoken')
        }),
        ('Schedule', {
            'fields': (
                ('monday_start', 'monday_end'),
                ('tuesday_start', 'tuesday_end'),
                ('wednesday_start', 'wednesday_end'),
                ('thursday_start', 'thursday_end'),
                ('friday_start', 'friday_end'),
                ('saturday_start', 'saturday_end'),
                ('sunday_start', 'sunday_end'),
            ),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Doctor Name'
