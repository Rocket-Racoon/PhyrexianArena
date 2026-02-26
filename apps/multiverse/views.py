from typing import Any
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Profile

# Create your views here.
class LandingPageView(TemplateView):
    template_name = 'multiverse/landing.html'
    

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'multiverse/dashboard.html'
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        context['profile'] = profile
        return context
        
        
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'multiverse/profile_view.html'
    context_object_name = 'user_profile'
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return self.request.user.profile
        return get_object_or_404(Profile, pk=pk)
    

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'multiverse/profile_update.html'
    fields = [
        'bio', 'location', 'avatar_url', 
        'twitch', 'instagram', 'tiktok', 'facebook'
    ]
    success_url = reverse_lazy('multiverse:profile_self')
    
    def get_object(self):
        return self.request.user.profile
    
    