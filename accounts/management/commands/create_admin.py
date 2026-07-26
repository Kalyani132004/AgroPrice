import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create admin user"

    def handle(self, *args, **kwargs):

        username = "AgroPrice"
        email = "agroprice@gmail.com"
        password = os.environ.get("ADMIN_PASSWORD")

        if not password:
            self.stdout.write(
                self.style.ERROR("ADMIN_PASSWORD missing")
            )
            return

        if not User.objects.filter(username=username).exists():

            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )

            self.stdout.write(
                self.style.SUCCESS("Admin created")
            )

        else:
            self.stdout.write(
                "Admin already exists"
            )