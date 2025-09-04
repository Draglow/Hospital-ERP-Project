from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('', views.invoice_list_view, name='invoice_list'),
    path('add/', views.invoice_add_view, name='invoice_add'),
    path('<int:pk>/', views.invoice_detail_view, name='invoice_detail'),
    path('<int:pk>/edit/', views.invoice_edit_view, name='invoice_edit'),
    path('<int:pk>/pay/', views.invoice_pay_view, name='invoice_pay'),
    path('<int:pk>/pdf/', views.invoice_pdf_view, name='invoice_pdf'),
]
