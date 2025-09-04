"""
URL configuration for hospital_erp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='homepage/index.html'), name='homepage'),
    path('developer/', TemplateView.as_view(template_name='developer_info.html'), name='developer_info'),
    path('logout-test/', TemplateView.as_view(template_name='logout_test.html'), name='logout_test'),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('patients.urls')),
    path('appointments/', include('appointments.urls')),
    path('doctors/', include('doctors.urls')),
    path('billing/', include('billing.urls')),
    path('pharmacy/', include('pharmacy.urls')),
    path('notifications/', include('notifications.urls')),
    path('api/', include('accounts.api_urls')),

    # Override admin logout to redirect to homepage
    path('admin/logout/', RedirectView.as_view(url='/', permanent=False), name='admin_logout_override'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
