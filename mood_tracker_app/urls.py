from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about_us, name='about_us'), 
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('check-in/', views.check_in_view, name='check_in'),
    path('history/', views.history_view, name='history'),
]