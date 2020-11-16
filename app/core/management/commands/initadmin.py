from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):
    help = "Create admin-superuser."

    def handle(self, *args, **options):
        email = 'admin@admin.com'
        admin = User.objects.filter(email='admin@admin.com')
        if not admin.exists():
            admin = User.objects.create(
                email='admin@admin.com'
            )
            admin.set_password('admin')
            admin.is_superuser = True
            admin.is_active = True
            admin.is_staff = True
            admin.save()
        else:
            print('Admin account inited yet.')
