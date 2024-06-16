from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Создание superuser"""

    def handle(self, *args, **options):
        user = User.objects.create(email="admin2@sky.pro")
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.set_password("spanky290195")
        user.save()
        print("Суперпользователь создан успешно!")
