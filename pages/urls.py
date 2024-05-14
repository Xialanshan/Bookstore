from django.urls import path
from .views import HomePageView, AboutPageView, AccountInformationView
from allauth.account.views import PasswordChangeView
from django.urls import reverse_lazy

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name='about'),
    path('information/', AccountInformationView.as_view(), name='information'),
    path('accounts/password/change/', PasswordChangeView.as_view(success_url=reverse_lazy('information')), name='password_change'),
]
