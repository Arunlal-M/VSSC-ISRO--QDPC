from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.apps import apps
from qdpc.core.constants import DEFAULT_AUTH_GROUPS


class Command(BaseCommand):
    help = 'Reseed Django auth groups with specific role names'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually doing it',
        )
        parser.add_argument(
            '--preserve-existing',
            action='store_true',
            help='Keep existing groups and only add missing ones',
        )
        parser.add_argument(
            '--add-permissions',
            action='store_true',
            help='Add basic permissions to the groups',
        )
        parser.add_argument(
            '--defaults-only',
            action='store_true',
            help='Seed only the minimal default groups (no extended role set)',
        )

    def handle(self, *args, **options):
        self.dry_run = options['dry_run']
        self.preserve_existing = options['preserve_existing']
        self.add_permissions = options['add_permissions']
        self.defaults_only = options['defaults_only']

        if self.dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))

        self.stdout.write('Reseeding Django auth groups...')

        # Clear existing groups first (unless preserving)
        if not self.preserve_existing:
            self.clear_existing_groups()

        # Create new groups
        self.create_new_groups()

        # Add permissions if requested
        if self.add_permissions:
            self.add_basic_permissions()

        if not self.dry_run:
            self.stdout.write(self.style.SUCCESS('Auth groups reseeded successfully!'))
        else:
            self.stdout.write(self.style.SUCCESS('Dry run completed - no changes made'))

    def clear_existing_groups(self):
        """Clear all existing auth groups"""
        if self.dry_run:
            group_count = Group.objects.count()
            self.stdout.write(f'Would delete {group_count} existing groups')
            return

        self.stdout.write('Clearing existing auth groups...')

        # Get count before deletion
        group_count = Group.objects.count()

        # Delete all groups
        Group.objects.all().delete()

        self.stdout.write(f'  ✓ Deleted {group_count} existing groups')

    def create_new_groups(self):
        """Create new auth groups with the specified names"""
        self.stdout.write('Creating new auth groups...')

        # Define the group names
        if self.defaults_only:
            group_names = DEFAULT_AUTH_GROUPS
        else:
            group_names = [
                # Guest role
                'Guest',

                # In-house/Project roles
                'Roles- In house process',
                'DPD Project',
                'Engineer Project',

                # SDA roles
                'Division Head SDA',
                'Section Head SDA',
                'Engineer SDA',
                'Technical/Scientific staff SDA',
                'Operator/Technicians SDA',

                # QA roles
                'Division Head QA',
                'Section Head QA',
                'Engineer QA',
                'Technical/Scientific staff QA',

                # QC roles
                'Division Head QC',
                'Section Head QC',
                'Engineer QC',
                'Technical/Scientific staff QC',

                # Testing agency roles
                'Division Head Testing agency',
                'Section Head Testing agency',
                'Engineer Testing agency',
                'Technical/Scientific staff Testing agency',

                # LSC roles
                'Member secretary, LSC',
                'Chairman, LSC',

                # NCRB roles
                'Member secretary, NCRB',
                'Chairman, NCRB',

                # Industry process roles
                'Roles- Industry process',
                'Operator/Technician industry',
                'Process Manager industry',
                'QC Manager industry',
                'QA Manager industry',

                # GOCO roles
                'Roles- GOCO',
                'GOCO operator',
                'GOCO supervisor',

                # System administrator roles
                'Roles- System administrator',
                'Master Admin/Super Admin',
                'System Administrator-1',
                'System Administrator-2',
                'System Administrator-3'
            ]

        created_count = 0
        existing_count = 0

        with transaction.atomic():
            for group_name in group_names:
                try:
                    if self.preserve_existing:
                        group, created = Group.objects.get_or_create(name=group_name)
                        if created:
                            created_count += 1
                            self.stdout.write(f'  ✓ Created group: {group_name}')
                        else:
                            existing_count += 1
                            self.stdout.write(f'  - Group already exists: {group_name}')
                    else:
                        # Replace-if-exists: delete any existing group with the same name, then create
                        if not self.dry_run:
                            Group.objects.filter(name=group_name).delete()
                            Group.objects.create(name=group_name)
                        created_count += 1
                        self.stdout.write(f'  ✓ Created group: {group_name}')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  ⚠ Failed to create group "{group_name}": {e}'))

        if self.preserve_existing:
            self.stdout.write(f'Created {created_count} new groups, {existing_count} already existed')
        else:
            self.stdout.write(f'Successfully created {created_count} new auth groups')

    def add_basic_permissions(self):
        """Add basic permissions to the groups"""
        if self.dry_run:
            self.stdout.write('Would add basic permissions to groups')
            return

        self.stdout.write('Adding basic permissions to groups...')

        # Get common content types for basic permissions
        content_types = ContentType.objects.filter(
            app_label__in=['qdpc_core_models', 'product', 'component', 'consumable', 'equipment']
        )

        # Get basic permissions
        permissions = Permission.objects.filter(
            content_type__in=content_types,
            codename__in=['view', 'add', 'change']
        )

        # Define permission levels for different group types
        permission_levels = {
            'Guest': ['view'],
            'DPD Project': ['view', 'add'],
            'Division Head SDA': ['view', 'add', 'change'],
            'Section Head SDA': ['view', 'add', 'change'],
            'Engineer SDA': ['view', 'add', 'change'],
            'Technical/Scientific staff SDA': ['view', 'add'],
            'Operator/Technicians SDA': ['view', 'add'],
            'Division Head QA': ['view', 'add', 'change'],
            'Section Head QA': ['view', 'add', 'change'],
            'Engineer QA': ['view', 'add', 'change'],
            'Technical/Scientific staff QA': ['view', 'add'],
            'Division Head QC': ['view', 'add', 'change'],
            'Section Head QC': ['view', 'add', 'change'],
            'Engineer QC': ['view', 'add', 'change'],
            'Technical/Scientific staff QC': ['view', 'add'],
            'Division Head Testing agency': ['view', 'add', 'change'],
            'Section Head Testing agency': ['view', 'add', 'change'],
            'Engineer Testing agency': ['view', 'add', 'change'],
            'Technical/Scientific staff Testing agency': ['view', 'add'],
            'Member secretary, LSC': ['view', 'add', 'change'],
            'Chairman, LSC': ['view', 'add', 'change'],
            'Member secretary, NCRB': ['view', 'add', 'change'],
            'Chairman, NCRB': ['view', 'add', 'change'],
            'Roles- Industry process': ['view', 'add', 'change'],
            'Operator/Technician industry': ['view', 'add'],
            'Process Manager industry': ['view', 'add', 'change'],
            'QC Manager industry': ['view', 'add', 'change'],
            'QA Manager industry': ['view', 'add', 'change'],
            'Roles- GOCO': ['view', 'add', 'change'],
            'GOCO operator': ['view', 'add'],
            'GOCO supervisor': ['view', 'add', 'change'],
            'Roles- System administrator': ['view', 'add', 'change'],
            'Master Admin/Super Admin': ['view', 'add', 'change', 'delete'],
            'System Administrator-1': ['view', 'add', 'change'],
            'System Administrator-2': ['view', 'add', 'change'],
            'System Administrator-3': ['view', 'add', 'change']
        }

        for group_name, permission_codes in permission_levels.items():
            try:
                group = Group.objects.get(name=group_name)
                group_permissions = permissions.filter(codename__in=permission_codes)
                group.permissions.set(group_permissions)
                self.stdout.write(f'  ✓ Added permissions to {group_name}')
            except Group.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ⚠ Group not found: {group_name}'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ⚠ Failed to add permissions to {group_name}: {e}'))
