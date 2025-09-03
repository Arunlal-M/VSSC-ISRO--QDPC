from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Reset the seeding completion flag to allow re-seeding'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force reset without confirmation',
        )

    def handle(self, *args, **options):
        seeding_key = 'qdpc_seeding_completed'
        
        if not options['force']:
            self.stdout.write(
                self.style.WARNING(
                    'This will reset the seeding flag and allow re-seeding on next migration. '
                    'Are you sure? (y/N): '
                )
            )
            response = input().lower().strip()
            if response not in ['y', 'yes']:
                self.stdout.write('Operation cancelled.')
                return

        # Clear the seeding flag
        cache.delete(seeding_key)
        
        self.stdout.write(
            self.style.SUCCESS(
                'Seeding flag has been reset. Seeding will run again on next migration.'
            )
        )
