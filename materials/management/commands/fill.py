from django.core.management.base import BaseCommand, call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command("loaddata", "/fixtures/data.json")
