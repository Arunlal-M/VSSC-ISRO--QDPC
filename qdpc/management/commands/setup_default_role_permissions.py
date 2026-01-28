from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.db import transaction
from qdpc.core.constants import DEFAULT_AUTH_GROUPS
from qdpc.models.page_permission import Page, PagePermission


class Command(BaseCommand):
    help = 'Set up default page permissions for all user roles with specific page access as per VSSC requirements'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually doing it',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreation of permissions even if they exist',
        )

    def handle(self, *args, **options):
        self.dry_run = options['dry_run']
        self.force = options['force']

        if self.dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))

        self.stdout.write('Setting up default page permissions for VSSC roles...')

        # Create groups if they don't exist
        self.create_missing_groups()

        # Create pages if they don't exist
        self.create_missing_pages()

        # Set up page permissions for each role
        self.setup_role_permissions()

        if not self.dry_run:
            self.stdout.write(self.style.SUCCESS('Default page permissions set up successfully!'))
        else:
            self.stdout.write(self.style.SUCCESS('Dry run completed - no changes made'))

    def create_missing_groups(self):
        """Create any missing auth groups"""
        self.stdout.write('Creating missing auth groups...')
        
        created_count = 0
        existing_count = 0

        with transaction.atomic():
            for group_name in DEFAULT_AUTH_GROUPS:
                try:
                    group, created = Group.objects.get_or_create(name=group_name)
                    if created:
                        created_count += 1
                        self.stdout.write(f'  ✓ Created group: {group_name}')
                    else:
                        existing_count += 1
                        self.stdout.write(f'  - Group already exists: {group_name}')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  ⚠ Failed to create group "{group_name}": {e}'))

        self.stdout.write(f'Groups: {created_count} created, {existing_count} already existed')

    def create_missing_pages(self):
        """Create all the required pages (1-25) if they don't exist"""
        self.stdout.write('Creating/updating required pages...')
        
        # Define all pages as per VSSC requirements
        required_pages = [
            # Product Data Management
            (1, 'Dashboard', '/dashboard/', 'Product Data Management', 'home', 'Main dashboard page'),
            (2, 'Equipments', '/equipment/', 'Product Data Management', 'tool', 'Equipment management'),
            (3, 'Acceptance Test', '/acceptance-test/', 'Product Data Management', 'check-circle', 'Acceptance test management'),
            (4, 'Rawmaterial', '/rawmaterial/', 'Product Data Management', 'package', 'Raw material management'),
            (5, 'Rawmaterial Batch', '/rawmaterial-batch/', 'Product Data Management', 'layers', 'Raw material batch management'),
            (6, 'Consumable', '/consumable/', 'Product Data Management', 'box', 'Consumable management'),
            (7, 'Consumable Batch', '/consumable-batch/', 'Product Data Management', 'archive', 'Consumable batch management'),
            (8, 'Component', '/component/', 'Product Data Management', 'cpu', 'Component management'),
            (9, 'Component Batch', '/component-batch/', 'Product Data Management', 'hard-drive', 'Component batch management'),
            (10, 'Process', '/process/', 'Product Data Management', 'settings', 'Process management'),
            (11, 'Product', '/product/', 'Product Data Management', 'shopping-bag', 'Product management'),
            (12, 'Product batch', '/product-batch/', 'Product Data Management', 'shopping-cart', 'Product batch management'),
            
            # Miscellaneous Data Management
            (13, 'Units', '/units/', 'Miscellaneous Data Management', 'hash', 'Units management'),
            (14, 'Grade', '/grade/', 'Miscellaneous Data Management', 'star', 'Grade management'),
            (15, 'Enduse', '/enduse/', 'Miscellaneous Data Management', 'target', 'End use management'),
            (16, 'Document Type', '/document-type/', 'Miscellaneous Data Management', 'file-text', 'Document type management'),
            (17, 'Center', '/center/', 'Miscellaneous Data Management', 'map-pin', 'Center management'),
            (18, 'Division', '/division/', 'Miscellaneous Data Management', 'git-branch', 'Division management'),
            (19, 'Source', '/source/', 'Miscellaneous Data Management', 'external-link', 'Source management'),
            (20, 'Supplier', '/supplier/', 'Miscellaneous Data Management', 'truck', 'Supplier management'),
            
            # User Management
            (21, 'Users', '/users/', 'User Management', 'users', 'User management'),
            
            # Report Generation
            (22, 'Process Log-Sheet', '/process-log-sheet/', 'Report Generation', 'clipboard', 'Process log sheet management'),
            (23, 'Stage Clearance', '/stage-clearance/', 'Report Generation', 'unlock', 'Stage clearance management'),
            (24, 'Q.A.R-Report', '/qar-report/', 'Report Generation', 'file-text', 'QAR report management'),
            
            # Roles Management
            (25, 'Groups', '/groups/', 'Roles Management', 'users', 'Group management'),
        ]
        
        created_count = 0
        updated_count = 0
        existing_count = 0

        with transaction.atomic():
            for page_id, name, url, section, icon, description in required_pages:
                try:
                    page, created = Page.objects.get_or_create(
                        page_id=page_id,
                        defaults={
                            'name': name,
                            'url': url,
                            'section': section,
                            'icon': icon,
                            'description': description,
                            'is_active': True
                        }
                    )
                    
                    if created:
                        created_count += 1
                        self.stdout.write(f'  ✓ Created page: {name} (ID: {page_id})')
                    else:
                        # Update existing page if needed
                        if (page.name != name or page.url != url or page.section != section or 
                            page.icon != icon or page.description != description):
                            page.name = name
                            page.url = url
                            page.section = section
                            page.icon = icon
                            page.description = description
                            page.save()
                            updated_count += 1
                            self.stdout.write(f'  ✓ Updated page: {name} (ID: {page_id})')
                        else:
                            existing_count += 1
                            self.stdout.write(f'  - Page already exists: {name} (ID: {page_id})')
                            
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  ⚠ Failed to create/update page "{name}": {e}'))

        self.stdout.write(f'Pages: {created_count} created, {updated_count} updated, {existing_count} already existed')

    def setup_role_permissions(self):
        """Set up specific page permissions for each role as per VSSC requirements"""
        self.stdout.write('Setting up role page permissions...')

        # Get all pages
        pages = Page.objects.filter(is_active=True).order_by('page_id')
        
        if not pages.exists():
            self.stdout.write(self.style.ERROR('No pages found. Please create pages first.'))
            return

        # Define role-specific permission sets as per VSSC requirements
        role_permissions = {
            # Guest role - minimal access (view only)
            'Guest': {
                'pages': [1],  # Dashboard only
                'permissions': ['view'],
                'description': 'Read-only access to dashboard only'
            },
            
            # In house process roles
            'Roles- In house process': {
                'pages': [1],  # Dashboard only
                'permissions': ['view'],
                'description': 'Basic access for in-house processes'
            },

            'DPD Project': {
                'pages': [1],  # Dashboard only
                'permissions': ['view'],
                'description': 'Basic access for DPD project work'
            },

            'Engineer Project': {
                'pages': [1],  # Dashboard only
                'permissions': ['view'],
                'description': 'Basic access for project work'
            },

            # SDA roles - full access to specified pages (1,5,7,9,12,22)
            'Division Head SDA': {
                'pages': [1, 5, 7, 9, 12, 22],
                'permissions': ['view', 'add', 'edit', 'approve'],
                'description': 'Can add new batches, approve/reject submissions, send for QA review'
            },

            'Section Head SDA': {
                'pages': [1, 5, 7, 9, 12, 22],
                'permissions': ['view', 'add', 'edit', 'approve'],
                'description': 'Can add new batches, approve/reject submissions, submit to Division Head'
            },

            'Engineer SDA': {
                'pages': [1, 5, 7, 9, 12, 22],
                'permissions': ['view', 'add', 'edit'],
                'description': 'Can add new batches, submit to Section Head'
            },

            'Technical/Scientific staff SDA': {
                'pages': [1, 5, 7, 9, 12, 22],
                'permissions': ['view', 'add', 'edit'],
                'description': 'Can add new batches, submit to Section Head'
            },

            'Operator/Technicians SDA': {
                'pages': [1, 5, 7, 9, 12, 22],
                'permissions': ['view', 'add', 'edit'],
                'description': 'Can add new batches, submit to Section Head'
            },

            # QA roles - access to pages 1,12,23,24
            'Division Head QA': {
                'pages': [1, 12, 23, 24],
                'permissions': ['view', 'add', 'edit', 'approve'],
                'description': 'Approve/reject the Section head QA/Engineer QA submissions'
            },

            'Section Head QA': {
                'pages': [1, 12, 23, 24],
                'permissions': ['view', 'add', 'edit', 'approve'],
                'description': 'Submit to Division head QA/ Reject Engineer QA/Technical/Scientific staff QA submissions'
            },

            'Engineer QA': {
                'pages': [1, 12, 23, 24],
                'permissions': ['view', 'add', 'edit'],
                'description': 'Submit to Section head QA'
            },

            'Technical/Scientific staff QA': {
                'pages': [1, 12, 23, 24],
                'permissions': ['view', 'add', 'edit'],
                'description': 'Submit to Section head QA'
            },

            # QC roles - access to pages 1,12
            'Division Head QC': {
                'pages': [1, 12],
                'permissions': ['view', 'add', 'edit', 'approve'],
                'description': 'Approve/reject the Section head QC/Engineer QC submissions'
            },

            'Section Head QC': {
                'pages': [1, 12],
                'permissions': ['view', 'add', 'edit', 'approve'],
                'description': 'Submit to Division head QC/ Reject Engineer QC/Technical/Scientific staff QC submissions'
            },

            'Engineer QC': {
                'pages': [1, 12],
                'permissions': ['view', 'add', 'edit'],
                'description': 'Submit to Section head QC'
            },

            'Technical/Scientific staff QC': {
                'pages': [1, 12],
                'permissions': ['view', 'add', 'edit'],
                'description': 'Submit to Section head QC'
            },

            # Testing agency roles - access to pages 1,5,7,9,12
            'Division Head Testing agency': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit', 'approve'],
                'description': 'Approve/reject the Section head Testing agency/Engineer Testing agency submissions'
            },

            'Section Head Testing agency': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit', 'approve'],
                'description': 'Submit to Division head Testing agency/ Reject Engineer Testing agency/Technical/Scientific staff Testing agency submissions'
            },

            'Engineer Testing agency': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit'],
                'description': 'Submit to Section head Testing agency'
            },

            'Technical/Scientific staff Testing agency': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit'],
                'description': 'Submit to Section head Testing agency'
            },

            # LSC roles - Guest access (will be added in next updates)
            'Member secretary, LSC': {
                'pages': [1],  # Dashboard only for now
                'permissions': ['view'],
                'description': 'Guest access (will be added in next updates)'
            },

            'Chairman, LSC': {
                'pages': [1],  # Dashboard only for now
                'permissions': ['view'],
                'description': 'Guest access (will be added in next updates)'
            },

            # NCRB roles - Guest access (will be added in next updates)
            'Member secretary, NCRB': {
                'pages': [1],  # Dashboard only for now
                'permissions': ['view'],
                'description': 'Guest access (will be added in next updates)'
            },

            'Chairman, NCRB': {
                'pages': [1],  # Dashboard only for now
                'permissions': ['view'],
                'description': 'Guest access (will be added in next updates)'
            },

            # Industry process roles - access to pages 1,5,7,9,12
            'Roles- Industry process': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit', 'approve'],
                'description': 'Full access to industry processes'
            },

            'Operator/Technician industry': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit'],
                'description': 'Basic access to industry processes'
            },

            'Process Manager industry': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit', 'approve'],
                'description': 'Full access to industry processes'
            },

            'QC Manager industry': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit', 'approve'],
                'description': 'Full access to QC industry processes'
            },

            'QA Manager industry': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit', 'approve'],
                'description': 'Full access to QA industry processes'
            },

            # GOCO roles - access to pages 1,5,7,9,12
            'Roles- GOCO': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit', 'approve'],
                'description': 'Full access to GOCO processes'
            },

            'GOCO operator': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit'],
                'description': 'Basic access to GOCO processes'
            },

            'GOCO supervisor': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit', 'approve'],
                'description': 'Full access to GOCO processes'
            },

            # System administrator roles - full access to all pages
            'Roles- System administrator': {
                'pages': list(range(1, 26)),  # All pages 1-25
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
                'description': 'All Pages, Can assign other admins, Can approve roles'
            },

            'Master Admin/Super Admin': {
                'pages': list(range(1, 26)),  # All pages 1-25
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
                'description': 'All Pages, Can assign other admins, Can approve roles'
            },

            'System Administrator-1': {
                'pages': list(range(1, 26)),  # All pages 1-25
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
                'description': 'All Pages'
            },

            'System Administrator-2': {
                'pages': list(range(1, 26)),  # All pages 1-25
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
                'description': 'All Pages'
            },

            'System Administrator-3': {
                'pages': list(range(1, 26)),  # All pages 1-25
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
                'description': 'All Pages'
            },

            # Default for any other roles not explicitly defined
            'default': {
                'pages': [1],  # Dashboard only
                'permissions': ['view'],
                'description': 'Basic read-only access to dashboard'
            }
        }

        # Set up permissions for each role
        for group_name in DEFAULT_AUTH_GROUPS:
            try:
                group = Group.objects.get(name=group_name)
                role_config = role_permissions.get(group_name, role_permissions['default'])
                self.setup_group_page_permissions(group, pages, role_config)
            except Group.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ⚠ Group not found: {group_name}'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ⚠ Failed to set up permissions for {group_name}: {e}'))

    def setup_group_page_permissions(self, group, pages, role_config):
        """Set up page permissions for a specific group"""
        if self.dry_run:
            self.stdout.write(f'  Would set up permissions for {group.name}: {role_config["permissions"]} on pages {role_config["pages"]}')
            return

        # Clear existing permissions for this group if force is enabled
        if self.force:
            PagePermission.objects.filter(group=group).delete()
            self.stdout.write(f'  Cleared existing permissions for {group.name}')

        # Add new permissions
        permissions_created = 0
        permissions_existing = 0

        # Get the specific pages this role should have access to
        role_pages = [p for p in pages if p.page_id in role_config['pages']]

        for page in role_pages:
            for permission_type in role_config['permissions']:
                try:
                    permission, created = PagePermission.objects.get_or_create(
                        group=group,
                        page_name=page.name,
                        page_url=page.url,
                        permission_type=permission_type,
                        defaults={
                            'is_active': True
                        }
                    )
                    
                    if created:
                        permissions_created += 1
                    else:
                        permissions_existing += 1
                        
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'    ⚠ Error creating permission {permission_type} for {page.name}: {e}'))

        self.stdout.write(f'  ✓ Set up permissions for {group.name}: {permissions_created} created, {permissions_existing} already existed')

    def get_permission_summary(self):
        """Get a summary of permissions for each group"""
        self.stdout.write('\nPermission Summary:')
        self.stdout.write('=' * 50)
        
        for group_name in DEFAULT_AUTH_GROUPS:
            try:
                group = Group.objects.get(name=group_name)
                perm_count = PagePermission.objects.filter(group=group).count()
                self.stdout.write(f'{group_name}: {perm_count} page permissions')
            except Group.DoesNotExist:
                self.stdout.write(f'{group_name}: Group not found')
            except Exception as e:
                self.stdout.write(f'{group_name}: Error - {e}')
