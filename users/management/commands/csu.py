from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@sky.pro',
            first_name='Admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True,
        )

        user.set_password('1100')
        user.save()

        user2 = User.objects.create(
            email='user@sky.pro',
            first_name='Manager',
            last_name='SkyPro',
            is_staff=False,
            is_superuser=False,
        )

        user2.set_password('1100')
        user2.save()

        user3 = User.objects.create(
            email='content-manager@sky.pro',
            first_name='Content-manager',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=False,
        )

        user3.set_password('1100')
        user3.save()

