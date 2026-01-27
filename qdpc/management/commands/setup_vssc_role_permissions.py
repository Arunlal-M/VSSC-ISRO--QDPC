from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.db import transaction
from qdpc.models.page_permission import Page, PagePermission


class Command(BaseCommand):
    help = 'Setup comprehensive VSSC role-based page permissions for all specified roles'

    def handle(self, *args, **options):
        self.stdout.write('Setting up VSSC role-based page permissions...')
        
        # Define all VSSC pages with their IDs
        vssc_pages = {
            1: 'Dashboard',
            2: 'Equipments',
            3: 'Acceptance Test',
            4: 'Rawmaterial',
            5: 'Rawmaterial Batch',
            6: 'Consumable',
            7: 'Consumable Batch',
            8: 'Component',
            9: 'Component Batch',
            10: 'Process',
            11: 'Product',
            12: 'Product Batch',
            13: 'Units',
            14: 'Grade',
            15: 'Enduse',
            16: 'Document Type',
            17: 'Center',
            18: 'Division',
            19: 'Source',
            20: 'Supplier',
            21: 'Users',
            22: 'Process Log-Sheet',
            23: 'Stage Clearance',
            24: 'Q.A.R-Report',
            25: 'Groups'
        }
        
        # Define role permissions based on the requirements
        role_permissions = {
            # SDA Roles
            'Division Head SDA': {
                'pages': [1, 5, 7, 9, 12, 22],
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
                'description': 'Can add a new batch and approve/reject the Section head SDA/Engineer SDA submissions and sends for QA review after approval'
            },
            'Section Head SDA': {
                'pages': [1, 5, 7, 9, 12, 22],
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
                'description': 'Can add a new batch and approve/reject the Engineer SDA/ Technical/Scientific staff SDA/Operator/Technicians SDA submissions and submit to Division Head SDA'
            },
            'Engineer SDA': {
                'pages': [1, 5, 7, 9, 12, 22],
                'permissions': ['view', 'add', 'edit'],
                'description': 'Can add a new batch and submit to Section head SDA'
            },
            'Technical/Scientific staff SDA': {
                'pages': [1, 5, 7, 9, 12, 22],
                'permissions': ['view', 'add', 'edit'],
                'description': 'Can add a new batch and submit to Section head SDA'
            },
            'Operator/Technicians SDA': {
                'pages': [1, 5, 7, 9, 12, 22],
                'permissions': ['view', 'add', 'edit'],
                'description': 'Can add a new batch and submit to Section head SDA'
            },
            
            # QA Roles
            'Division Head QA': {
                'pages': [1, 12, 23, 24],
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
                'description': 'Approve/reject the Section head QA/Engineer QA submissions'
            },
            'Section Head QA': {
                'pages': [1, 12, 23, 24],
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
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
            
            # QC Roles
            'Division Head QC': {
                'pages': [1, 12],
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
                'description': 'Approve/reject the Section head QC/Engineer QC submissions'
            },
            'Section Head QC': {
                'pages': [1, 12],
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
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
            
            # Testing Agency Roles
            'Division Head Testing agency': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
                'description': 'Approve/reject the Section head Testing agency/Engineer Testing agency submissions'
            },
            'Section Head Testing agency': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
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
            
            # Industry Roles
            'Operator/Technician industry': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit'],
                'description': 'Industry operator/technician permissions'
            },
            'Process Manager industry': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit', 'delete'],
                'description': 'Industry process manager permissions'
            },
            'QC Manager industry': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
                'description': 'Industry QC manager permissions'
            },
            'QA Manager industry': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
                'description': 'Industry QA manager permissions'
            },
            
            # GOCO Roles
            'GOCO operator': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit'],
                'description': 'GOCO operator permissions'
            },
            'GOCO supervisor': {
                'pages': [1, 5, 7, 9, 12],
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
                'description': 'GOCO supervisor permissions'
            },
            
            # System Administrator Roles
            'Master Admin/Super Admin': {
                'pages': list(range(1, 26)),  # All pages
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
                'description': 'All Pages, Can assign other admins, Can approve roles'
            },
            'System Administrator-1': {
                'pages': list(range(1, 26)),  # All pages
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
                'description': 'All Pages'
            },
            'System Administrator-2': {
                'pages': list(range(1, 26)),  # All pages
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
                'description': 'All Pages'
            },
            'System Administrator-3': {
                'pages': list(range(1, 26)),  # All pages
                'permissions': ['view', 'add', 'edit', 'delete', 'approve'],
                'description': 'All Pages'
            }
        }
        
        with transaction.atomic():
            # Create or get all pages
            created_pages = {}
            for page_id, page_name in vssc_pages.items():
                page, created = Page.objects.get_or_create(
                    name=page_name,
                    defaults={
                        'url': f'page-{page_id}',
                        'description': f'VSSC {page_name} page'
                    }
                )
                created_pages[page_id] = page
                if created:
                    self.stdout.write(f'Created page: {page_name} (ID: {page_id})')
            
            # Create or get all groups and set permissions
            for role_name, role_config in role_permissions.items():
                group, created = Group.objects.get_or_create(name=role_name)
                
                if created:
                    self.stdout.write(f'Created group: {role_name}')
                
                # Clear existing permissions for this group
                PagePermission.objects.filter(group=group).delete()
                
                # Set permissions for each page
                for page_id in role_config['pages']:
                    if page_id in created_pages:
                        page = created_pages[page_id]
                        
                        for permission_type in role_config['permissions']:
                            PagePermission.objects.create(
                                group=group,
                                page_name=page.name,
                                page_url=page.url,
                                permission_type=permission_type
                            )
                
                self.stdout.write(f'Set permissions for {role_name}: {len(role_config["pages"])} pages, {len(role_config["permissions"])} permission types')
                self.stdout.write(f'  Description: {role_config["description"]}')
        
        self.stdout.write(self.style.SUCCESS('Successfully set up VSSC role-based page permissions!'))
        
        # Display summary
        total_groups = Group.objects.count()
        total_pages = Page.objects.count()
        total_permissions = PagePermission.objects.count()
        
        self.stdout.write(f'\nSummary:')
        self.stdout.write(f'  Total Groups: {total_groups}')
        self.stdout.write(f'  Total Pages: {total_pages}')
        self.stdout.write(f'  Total Permissions: {total_permissions}')
