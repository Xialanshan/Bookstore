from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth.models import Permission

@receiver(user_signed_up)
def add_special_status_permission(request, user, **kwargs):
    try:
        permission = Permission.objects.get(codename='special_status', content_type__app_label='books')
        user.user_permissions.add(permission)
    except Permission.DoesNotExist:
        pass

    