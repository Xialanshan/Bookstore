from django.urls import path
from allauth.account.views import resend_email_confirmation, password_reset
from .views import SignupPageView

urlpatterns = [
    path("signup/",SignupPageView.as_view(), name='signup'),
    path('resend-verification/', resend_email_confirmation, name='account_resend_verification'),
    path('password/reset/', password_reset, name="account_reset_password"),  
]

