from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('debug/', views.notification_list_debug, name='notification_list_debug'),
    path('dropdown/', views.notification_dropdown, name='notification_dropdown'),
    path('mark-read/<int:pk>/', views.mark_as_read, name='mark_as_read'),
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('delete/<int:pk>/', views.delete_notification, name='delete_notification'),
    path('preferences/', views.notification_preferences, name='preferences'),
    path('mobile-text-test/', views.mobile_text_length_test, name='mobile_text_length_test'),
    path('mobile-buttons-test/', views.mobile_action_buttons_test, name='mobile_action_buttons_test'),
]
