from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointment_list_view, name='appointment_list'),
    path('add/', views.appointment_add_view, name='appointment_add'),
    path('<int:pk>/', views.appointment_detail_view, name='appointment_detail'),
    path('<int:pk>/edit/', views.appointment_edit_view, name='appointment_edit'),
    path('<int:pk>/cancel/', views.appointment_cancel_view, name='appointment_cancel'),
    path('<int:pk>/start/', views.appointment_start_view, name='appointment_start'),
    path('<int:pk>/complete/', views.appointment_complete_view, name='appointment_complete'),
    path('<int:pk>/cancel-ajax/', views.appointment_cancel_ajax_view, name='appointment_cancel_ajax'),
    path('check-availability/', views.check_doctor_availability, name='check_availability'),
    path('mobile-test/', views.mobile_test_view, name='mobile_test'),
    path('test-functionality/', views.test_functionality_view, name='test_functionality'),
]
