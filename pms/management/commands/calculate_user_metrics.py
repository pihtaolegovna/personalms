from django.core.management.base import BaseCommand
from pms.utils import calculate_user_metrics

class Command(BaseCommand):
    help = 'Calculate and update user task metrics'

    def handle(self, *args, **options):
        calculate_user_metrics()
        self.stdout.write(self.style.SUCCESS('User task metrics updated successfully.'))