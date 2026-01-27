from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from qdpc.models.page_permission import Page, PagePermission


class Command(BaseCommand):
    help = 'Create basic PagePermission records for a group'

    def add_arguments(self, parser):
        parser.add_argument('--group', type=str, required=True, help='Group name to create permissions for')
        parser.add_argument('--pages', nargs='+', help='Specific page names to create permissions for (default: all)')

    def handle(self, *args, **options):
        group_name = options['group']
        specific_pages = options['pages']
        
        try:
            group = Group.objects.get(name=group_name)
            self.stdout.write(f'✓ Found group: {group.name}')
        except Group.DoesNotExist:
            self.stdout.write(f'✗ Group "{group_name}" does not exist!')
            self.stdout.write('Available groups:')
            for g in Group.objects.all():
                self.stdout.write(f'  - {g.name}')
            return
        
        # Get all pages or specific pages
        if specific_pages:
            pages = Page.objects.filter(name__in=specific_pages, is_active=True)
            if not pages.exists():
                self.stdout.write(f'✗ No pages found with names: {specific_pages}')
                return
        else:
            pages = Page.objects.filter(is_active=True)
        
        self.stdout.write(f'\nCreating permissions for {pages.count()} pages...')
        
        # Clear existing permissions for this group
        existing_count = PagePermission.objects.filter(group=group).count()
        if existing_count > 0:
            PagePermission.objects.filter(group=group).delete()
            self.stdout.write(f'Cleared {existing_count} existing permissions for group: {group.name}')
        
        # Create view permissions for all pages
        created_count = 0
        for page in pages:
            # Create view permission
            permission, created = PagePermission.objects.get_or_create(
                group=group,
                page_name=page.name,
                page_url=page.url,
                permission_type='view',
                defaults={'is_active': True}
            )
            if created:
                created_count += 1
                self.stdout.write(f'  ✓ Created view permission for: {page.name}')
            
            # For some pages, also create add/edit permissions
            if page.name in ['Product', 'Rawmaterial', 'Consumable', 'Component']:
                for perm_type in ['add', 'edit']:
                    permission, created = PagePermission.objects.get_or_create(
                        group=group,
                        page_name=page.name,
                        page_url=page.url,
                        permission_type=perm_type,
                        defaults={'is_active': True}
                    )
                    if created:
                        created_count += 1
                        self.stdout.write(f'  ✓ Created {perm_type} permission for: {page.name}')
        
        self.stdout.write(f'\n✓ Created {created_count} permissions for group: {group.name}')
        
        # Show what was created
        group_permissions = PagePermission.objects.filter(group=group, is_active=True)
        if group_permissions.exists():
            self.stdout.write('\nCurrent permissions:')
            pages = {}
            for perm in group_permissions:
                if perm.page_name not in pages:
                    pages[perm.page_name] = []
                pages[perm.page_name].append(perm.permission_type)
            
            for page_name, perm_types in pages.items():
                self.stdout.write(f'  - {page_name}: {", ".join(perm_types)}')
        else:
            self.stdout.write('No permissions were created!')
        
        self.stdout.write('\nNow the sidebar should show these pages based on database permissions!')
