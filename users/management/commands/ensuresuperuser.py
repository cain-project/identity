from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            print("Superuser account found. Skipping superuser creation.")
            return

        password = User.objects.make_random_password(length=18)
        user = User.objects.create_superuser(given_name="Super", family_name="User",
                                             full_name="Default Super User",
                                             preferred_name="Super User",
                                             locale="en_GB",
                                             email="superuser@localhost",
                                             password=password)

        print("Created superuser account with the following credentials:")
        print("* Email address:", user.email)
        print("* Password:", password)
        print("Make sure to change the password ASAP.")
