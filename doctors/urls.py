from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.doctor_list_view, name='doctor_list'),
    path('add/', views.doctor_add_view, name='doctor_add'),
    path('<int:pk>/', views.doctor_detail_view, name='doctor_detail'),
    path('<int:pk>/edit/', views.doctor_edit_view, name='doctor_edit'),
    path('<int:pk>/schedule/', views.doctor_schedule_view, name='doctor_schedule'),
]
