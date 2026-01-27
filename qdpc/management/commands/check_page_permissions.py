from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from qdpc.models.page_permission import PagePermission


class Command(BaseCommand):
    help = 'Check PagePermission records for a specific group'

    def add_arguments(self, parser):
        parser.add_argument('--group', type=str, required=True, help='Group name to check permissions for')

    def handle(self, *args, **options):
        group_name = options['group']
        
        try:
            group = Group.objects.get(name=group_name)
            self.stdout.write(f'✓ Found group: {group.name}')
        except Group.DoesNotExist:
            self.stdout.write(f'✗ Group "{group_name}" does not exist!')
            self.stdout.write('Available groups:')
            for g in Group.objects.all():
                self.stdout.write(f'  - {g.name}')
            return
        
        # Check PagePermission records for this group
        self.stdout.write(f'\n=== PagePermission Records for {group.name} ===')
        permissions = PagePermission.objects.filter(group=group, is_active=True)
        
        if permissions.exists():
            self.stdout.write(f'Found {permissions.count()} PagePermission records:')
            
            # Group by page name
            pages = {}
            for perm in permissions:
                if perm.page_name not in pages:
                    pages[perm.page_name] = []
                pages[perm.page_name].append(perm.permission_type)
            
            for page_name, perm_types in pages.items():
                self.stdout.write(f'  - {page_name}: {", ".join(perm_types)}')
        else:
            self.stdout.write('No PagePermission records found!')
            self.stdout.write('\nThis means the sidebar will show NO pages except Dashboard.')
            self.stdout.write('You need to set permissions through the permission management interface.')
        
        # Show what the sidebar should display
        self.stdout.write(f'\n=== Expected Sidebar Display ===')
        if permissions.exists():
            self.stdout.write('Based on PagePermission records, sidebar should show:')
            
            # Map page names to sidebar sections
            sections = {
                'Equipments': 'Product Data Management',
                'Acceptance Test': 'Product Data Management',
                'Rawmaterial': 'Product Data Management', 
                'Consumable': 'Product Data Management',
                'Component': 'Product Data Management',
                'Process': 'Product Data Management',
                'Product': 'Product Data Management',
                'Center': 'Miscellaneous Data Management',
                'Division': 'Miscellaneous Data Management',
                'Users': 'User Management',
                'Process Log-Sheet': 'Report Generation',
                'Stage Clearance': 'Report Generation',
                'Groups': 'Roles Management'
            }
            
            view_permissions = permissions.filter(permission_type='view')
            for perm in view_permissions:
                section = sections.get(perm.page_name, 'Unknown')
                self.stdout.write(f'  ✓ {perm.page_name} ({section})')
        else:
            self.stdout.write('No pages will be shown in sidebar (only Dashboard)')
        
        self.stdout.write('\n=== End Check ===')
