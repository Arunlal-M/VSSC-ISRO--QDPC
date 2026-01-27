from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from qdpc.models.page_permission import Page, PagePermission
from qdpc.core.dynamic_sidebar_context import dynamic_sidebar_context, ROLE_PAGE_ACCESS


class Command(BaseCommand):
    help = 'Debug Division Head SDA permissions specifically'

    def handle(self, *args, **options):
        self.stdout.write('=== Division Head SDA Permission Debug ===\n')
        
        # Check if Division Head SDA group exists
        try:
            division_head_group = Group.objects.get(name='Division Head SDA')
            self.stdout.write(f'✓ Found Division Head SDA group: {division_head_group.name}')
        except Group.DoesNotExist:
            self.stdout.write('✗ Division Head SDA group does not exist!')
            return
        
        # Check what pages exist in the database
        self.stdout.write('\n=== Database Pages ===')
        pages = Page.objects.filter(is_active=True).order_by('page_id')
        self.stdout.write(f'Total active pages: {pages.count()}')
        for page in pages:
            self.stdout.write(f'  - {page.page_id}: {page.name} ({page.section})')
        
        # Check what PagePermission records exist for Division Head SDA
        self.stdout.write('\n=== PagePermission Records for Division Head SDA ===')
        permissions = PagePermission.objects.filter(group=division_head_group, is_active=True)
        if permissions.exists():
            self.stdout.write(f'Found {permissions.count()} PagePermission records:')
            for perm in permissions:
                self.stdout.write(f'  - {perm.page_name} ({perm.permission_type})')
        else:
            self.stdout.write('No PagePermission records found!')
        
        # Check the role-based fallback mapping
        self.stdout.write('\n=== Role-Based Fallback Mapping ===')
        if 'Division Head SDA' in ROLE_PAGE_ACCESS:
            allowed_pages = ROLE_PAGE_ACCESS['Division Head SDA']
            self.stdout.write(f'Allowed pages from role mapping: {allowed_pages}')
            
            # Check which of these pages actually exist in the database
            existing_page_names = [page.name for page in pages]
            self.stdout.write('\nMatching pages:')
            for allowed_page in allowed_pages:
                if allowed_page in existing_page_names:
                    self.stdout.write(f'  ✓ {allowed_page} - exists in database')
                else:
                    self.stdout.write(f'  ✗ {allowed_page} - NOT found in database')
        else:
            self.stdout.write('Division Head SDA not found in ROLE_PAGE_ACCESS!')
        
        # Check if there are any users in this group
        self.stdout.write('\n=== Users in Division Head SDA Group ===')
        users_in_group = User.objects.filter(groups=division_head_group)
        if users_in_group.exists():
            self.stdout.write(f'Found {users_in_group.count()} users in group:')
            for user in users_in_group:
                self.stdout.write(f'  - {user.username} (superuser: {user.is_superuser})')
                
                # Test the context processor for this user
                self.stdout.write(f'\n  Testing sidebar context for {user.username}:')
                from django.test import RequestFactory
                factory = RequestFactory()
                request = factory.get('/')
                request.user = user
                
                try:
                    context = dynamic_sidebar_context(request)
                    
                    # Show sidebar permissions
                    sidebar_permissions = {k: v for k, v in context.items() if k.startswith('can_access_')}
                    for perm_name, value in sidebar_permissions.items():
                        status = "✓" if value else "✗"
                        self.stdout.write(f'    {status} {perm_name}: {value}')
                        
                except Exception as e:
                    self.stdout.write(f'    ✗ Error generating context: {str(e)}')
        else:
            self.stdout.write('No users found in Division Head SDA group!')
        
        # Show what the sidebar should display based on role mapping
        self.stdout.write('\n=== Expected Sidebar Display ===')
        if 'Division Head SDA' in ROLE_PAGE_ACCESS:
            allowed_pages = ROLE_PAGE_ACCESS['Division Head SDA']
            self.stdout.write('Based on role mapping, sidebar should show:')
            
            # Map to sidebar sections
            sections = {
                'Dashboard': 'Pages',
                'Equipments': 'Product Data Management',
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
            
            for page in allowed_pages:
                section = sections.get(page, 'Unknown')
                self.stdout.write(f'  - {page} ({section})')
        
        self.stdout.write('\n=== End Debug ===')
