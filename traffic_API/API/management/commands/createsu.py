import os
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
admin = os.environ.get("ADMIN")
admin_email = os.environ.get("ADMIN_EMAIL")
admin_password = os.environ.get("ADMIN_PASSWORD")
print(admin, admin_email, admin_password)


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not get_user_model().objects.filter(email=admin_email).exists():
            get_user_model().objects.create_superuser(
                email=admin_email, password=admin_password, name=admin
            )
            self.stdout.write(
                self.style.SUCCESS("Successfully created superuser")
            )
