from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        name = options["username"]
        if args:
            name = args[0]
        self.stdout.write(f"Hello, {name}!")
        self.stdout.write("This is a test command.")
        return super().handle(*args, **options)
