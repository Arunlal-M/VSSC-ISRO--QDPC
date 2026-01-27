from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from qdpc_core_models.models.page_permission import PagePermission


class Command(BaseCommand):
    help = 'Setup default permissions for super admin and administrative roles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update existing permissions',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up default permissions for administrative roles...'))
        
        # Define administrative role names
        admin_roles = [
            'System Administrator',
            'Super Admin', 
            'SYSTEM ADMINISTRATOR',
            'SUPER ADMIN',
            'Master Admin/Super Admin',
            'Roles- System administrator',
            'System Administrator-1',
            'System Administrator-2', 
            'System Administrator-3'
        ]
        
        # Define all pages and their permissions
        pages_permissions = {
            'Dashboard': ['view'],
            'Equipment': ['view', 'add', 'edit', 'delete'],
            'Acceptance test': ['view', 'add', 'edit', 'delete', 'approve', 'reject'],
            'Raw material': ['view', 'add', 'edit', 'delete'],
            'Raw material batch': ['view', 'add', 'edit', 'delete'],
            'Consumable': ['view', 'add', 'edit', 'delete'],
            'Consumable batch': ['view', 'add', 'edit', 'delete'],
            'Component': ['view', 'add', 'edit', 'delete'],
            'Component batch': ['view', 'add', 'edit', 'delete'],
            'Product': ['view', 'add', 'edit', 'delete'],
            'Product batch': ['view', 'add', 'edit', 'delete', 'approve', 'reject'],
            'Process': ['view', 'add', 'edit', 'delete'],
            'Units': ['view', 'add', 'edit', 'delete'],
            'Grade': ['view', 'add', 'edit', 'delete'],
            'Enduse': ['view', 'add', 'edit', 'delete'],
            'Document type': ['view', 'add', 'edit', 'delete'],
            'Center': ['view', 'add', 'edit', 'delete'],
            'Division': ['view', 'add', 'edit', 'delete'],
            'Source': ['view', 'add', 'edit', 'delete'],
            'Supplier': ['view', 'add', 'edit', 'delete'],
            'User management': ['view', 'add', 'edit', 'delete'],
            'Reports': ['view', 'add'],
            'Stage clearance': ['view', 'add', 'edit', 'delete'],
            'QAR report': ['view', 'add'],
            'Role management': ['view', 'add', 'edit', 'delete'],
            'Permission management': ['view', 'edit']
        }
        
        created_count = 0
        updated_count = 0
        
        for role_name in admin_roles:
            # Get or create the group
            group, group_created = Group.objects.get_or_create(name=role_name)
            
            if group_created:
                self.stdout.write(f'Created group: {role_name}')
            
            # Set permissions for this group
            for page_name, actions in pages_permissions.items():
                for action in actions:
                    permission, created = PagePermission.objects.get_or_create(
                        group=group,
                        page_name=page_name,
                        action=action,
                        defaults={'is_allowed': True}
                    )
                    
                    if created:
                        created_count += 1
                        self.stdout.write(f'  ✓ Created: {role_name} - {page_name} - {action}')
                    elif options['force'] and not permission.is_allowed:
                        permission.is_allowed = True
                        permission.save()
                        updated_count += 1
                        self.stdout.write(f'  ✓ Updated: {role_name} - {page_name} - {action}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Created {created_count} permissions, Updated {updated_count} permissions'
            )
        )
        
        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write('ADMINISTRATIVE ROLES WITH FULL PERMISSIONS:')
        self.stdout.write('='*60)
        
        for role_name in admin_roles:
            try:
                group = Group.objects.get(name=role_name)
                perm_count = PagePermission.objects.filter(group=group, is_allowed=True).count()
                self.stdout.write(f'{role_name}: {perm_count} permissions')
            except Group.DoesNotExist:
                self.stdout.write(f'{role_name}: Group not found')
        
        self.stdout.write('\n' + self.style.SUCCESS('All administrative roles now have full permissions by default!'))
