from django.urls import path
from django.contrib.auth import views as AuthViews
from . import views

app_name = 'multiverse'

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile_self'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_view'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
]