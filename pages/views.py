from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import Group
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
        context['has_review_permission'] = self.request.user.has_perm('books.can_add_review')
        return context

class UpgradeToPremiumView(LoginRequiredMixin, View):
    template_name = 'upgrade_premium.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        next_url = request.GET.get('next', 'information')
        try:
            premium_group = Group.objects.get(name='Premium')
            request.user.groups.add(premium_group)
            messages.success(request, 'You have been successfully upgraded to a Premium member.')
        except Group.DoesNotExist:
            messages.error(request, 'The Premium group does not exist.')
        return redirect(next_url) 
    

