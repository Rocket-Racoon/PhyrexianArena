from typing import Any
from django.db.models import Max
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, UpdateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from config.constants import SetTypes
from .models import Profile
from apps.blind_eternities.models import Card


def debug_data(queryset, query):
    debug_data = queryset.values('name', 'reprint', 'variation', 'set__code', 'layout')
    print("\n" + "="*50)
    print(f"DEBUG: Resultados para '{query}'")
    for data in debug_data:
        print(f"Carta: {data['name']} | Set: {data['set__code']} | Reprint: {data['reprint']} | Variation: {data['variation']} | Layout {data['layout']}")
    print("="*50 + "\n")
    
        
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
    template_name = 'multiverse/profile_edit.html'
    fields = [
        'bio', 'location', 'avatar_url', 
        'twitch', 'instagram', 'tiktok', 'facebook'
    ]
    success_url = reverse_lazy('multiverse:profile_self')
    
    def get_object(self):
        return self.request.user.profile
    

class CardSearchView(ListView):
    model = Card
    template_name = 'multiverse/landing.html'
    context_object_name = 'results'
    paginate_by = 25
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        special_cards = self.request.GET.get('special_cards') == 'on'
        latest_version = self.request.GET.get('latest_version') == 'on'
        digital_version = self.request.GET.get('digital_version') == 'on'
        random_card = self.request.GET.get('random_card') == 'on'
        
        queryset = Card.objects.all().select_related('set')
        
        if not special_cards:
            excluded_types = [
                SetTypes.ART.value,
                SetTypes.FRONTCARDS.value,
                SetTypes.HEROES.value,
                SetTypes.TOKEN.value,
                SetTypes.MINIGAME,
                SetTypes.MEMORABILIA,
                SetTypes.PLANAR,
                SetTypes.SCHEMES
            ]
            queryset = queryset.exclude(set__set_type__in=excluded_types)
        
        if not digital_version:
            queryset = queryset.exclude(set__set_type__in=SetTypes.ALCHEMY.value)
            queryset = queryset.filter(digital=False)
        
        if latest_version:
            queryset = queryset.filter(reprint=False, variation=False)
            unique_ids = queryset.values('name').annotate(
                latest_id=Max('id')
            ).values_list('latest_id', flat=True)
            queryset = queryset.filter(id__in=unique_ids)
        
        # Search by name
        if query:
            queryset = queryset.filter(name__icontains=query).order_by('-released_at')
        elif random_card:
            queryset = queryset.order_by('?')[:25]
        else:
            queryset = queryset.order_by('-released_at')[:25]
            
        debug_data(queryset, query)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['special_cards'] = self.request.GET.get('special_cards') == 'on'
        context['latest_version'] = self.request.GET.get('latest_version') == 'on'
        context['digital_version'] = self.request.GET.get('digital_version') == 'on'
        context['random_card'] = self.request.GET.get('random_card') == 'on'
        return context