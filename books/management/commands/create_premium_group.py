from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from books.models import Review  

class Command(BaseCommand):
    help = 'Create the Premium group and assign can_add_review permission'

    def handle(self, *args, **kwargs):
        # 创建或获取 Premium 组
        premium_group, created = Group.objects.get_or_create(name='Premium')
        if created:
            self.stdout.write(self.style.SUCCESS(f'Group "Premium" created'))
        else:
            self.stdout.write(f'Group "Premium" already exists')
        
        # 获取 can_add_review 权限
        content_type = ContentType.objects.get_for_model(Review)
        permission, perm_created = Permission.objects.get_or_create(
            codename='can_add_review',
            name='Can add reviews nolimit',
            content_type=content_type
        )
        
        # 将权限添加到组
        premium_group.permissions.add(permission)
        
        if perm_created:
            self.stdout.write(self.style.SUCCESS(f'Permission "can_add_review" created and added to group "Premium"'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Permission "can_add_review" already exists and added to group "Premium"'))

        self.stdout.write(self.style.SUCCESS('Successfully created/updated the Premium group'))

