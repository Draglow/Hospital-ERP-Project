from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('mobile/', views.mobile_dashboard_view, name='mobile_dashboard'),
    path('responsive-test/', views.responsive_detection_test_view, name='responsive_detection_test'),
    path('mobile/test/', views.mobile_responsive_test_view, name='mobile_responsive_test'),
    path('mobile/navigation-test/', views.mobile_navigation_test_view, name='mobile_navigation_test'),
    path('mobile/crud-test/', views.mobile_crud_test_view, name='mobile_crud_test'),
    path('patients/', views.patient_list_view, name='patient_list'),
    path('patients/add/', views.patient_add_view, name='patient_add'),
    path('patients/<int:pk>/', views.patient_detail_view, name='patient_detail'),
    path('patients/<int:pk>/edit/', views.patient_edit_view, name='patient_edit'),
    path('patients/<int:pk>/delete/', views.patient_delete_view, name='patient_delete'),
    path('patients/export/', views.patient_export_view, name='patient_export'),
    path('patients/search/', views.patient_search_ajax, name='patient_search_ajax'),
    path('search/global/', views.global_search_ajax, name='global_search_ajax'),
    path('api/dashboard-stats/', views.dashboard_stats_api, name='dashboard_stats_api'),
]
