"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.admin import action
from django.urls import path

from notification.views import NotificationView
from transactions.views import TransactionViewSet, CachedReportView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("transactions/", TransactionViewSet.as_view(), name="transactions"),
    path('notification/send/', NotificationView.as_view(), name='notification-send'),

    path('transactions/cached-report',CachedReportView.as_view(), name='transactions-cached-report'),
]
