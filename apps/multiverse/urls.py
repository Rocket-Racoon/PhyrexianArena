from django.urls import path
from django.contrib.auth import views as AuthViews
from .views import *

app_name = 'multiverse'

urlpatterns = [
    # path('', LandingPageView.as_view(), name='landing'),
    path('', CardSearchView.as_view(), name='landing'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileDetailView.as_view(), name='profile_self'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_view'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
]