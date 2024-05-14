from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page    # new

class HomePageView(TemplateView):
    template_name = "home.html"

class AboutPageView(TemplateView):
    template_name = 'about.html'
    
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return cache_page(60 * 15)(view)

class AccountInformationView(LoginRequiredMixin, TemplateView):
    template_name = 'information.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.user.email
        return context


    
