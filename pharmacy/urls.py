from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('', views.medicine_list_view, name='medicine_list'),
    path('add/', views.medicine_add_view, name='medicine_add'),
    path('<int:pk>/', views.medicine_detail_view, name='medicine_detail'),
    path('<int:pk>/edit/', views.medicine_edit_view, name='medicine_edit'),
    path('<int:pk>/stock-adjustment/', views.stock_adjustment_view, name='stock_adjustment'),
    path('<int:pk>/adjust-stock-ajax/', views.stock_adjustment_ajax_view, name='stock_adjustment_ajax'),
    path('<int:pk>/stock-info-ajax/', views.medicine_stock_info_ajax, name='medicine_stock_info_ajax'),
    path('prescriptions/', views.prescription_list_view, name='prescription_list'),
    path('prescriptions/<int:pk>/dispense/', views.prescription_dispense_view, name='prescription_dispense'),
    path('reports/low-stock/', views.low_stock_report, name='low_stock_report'),
    path('reports/expiring/', views.expiring_medicines_report, name='expiring_report'),
    path('test-stock-functionality/', views.test_stock_functionality_view, name='test_stock_functionality'),
]
