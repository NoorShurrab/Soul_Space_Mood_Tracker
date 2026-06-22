"""
URL configuration for SoulSpaceProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from login_app import views 
from mood_tracker_app.api import mood_api, send_reminder_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login_app.urls')),
    path('mood/', include('mood_tracker_app.urls')),


    path('password_reset/', views.forgot_password, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reset/<str:token>/', views.reset_password_confirm, name='password_reset_confirm'),

    # ✅ API endpoints
    path('api/moods/', mood_api, name='mood_api'),
    path('api/send-reminder/', send_reminder_api, name='send_reminder'),
]