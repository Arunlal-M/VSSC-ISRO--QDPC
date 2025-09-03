from django.core.management.base import BaseCommand
from qdpc.models.page_permission import Page


class Command(BaseCommand):
    help = 'Seed VSSC pages into the database'

    def handle(self, *args, **options):
        self.stdout.write('Seeding VSSC pages...')
        
        # Define VSSC pages
        vssc_pages = [
            # Pages
            {'name': 'Dashboard', 'url': 'user-dashboard', 'section': 'Pages', 'page_id': 1, 'icon': 'home'},
            
            # Product Data Management
            {'name': 'Equipments', 'url': 'equipment-list', 'section': 'Product Data Management', 'page_id': 2, 'icon': 'tool'},
            {'name': 'Acceptance Test', 'url': 'acceptance-test-list', 'section': 'Product Data Management', 'page_id': 3, 'icon': 'check-circle'},
            {'name': 'Rawmaterial', 'url': 'raw-material', 'section': 'Product Data Management', 'page_id': 4, 'icon': 'package'},
            {'name': 'Rawmaterial Batch', 'url': 'raw-material-batch-fetch', 'section': 'Product Data Management', 'page_id': 5, 'icon': 'layers'},
            {'name': 'Consumable', 'url': 'consumable-list', 'section': 'Product Data Management', 'page_id': 6, 'icon': 'box'},
            {'name': 'Consumable Batch', 'url': 'consumable-batch-fetch', 'section': 'Product Data Management', 'page_id': 7, 'icon': 'archive'},
            {'name': 'Component', 'url': 'component-list', 'section': 'Product Data Management', 'page_id': 8, 'icon': 'cpu'},
            {'name': 'Component Batch', 'url': 'component-batch-fetch', 'section': 'Product Data Management', 'page_id': 9, 'icon': 'hard-drive'},
            {'name': 'Process', 'url': 'process_list', 'section': 'Product Data Management', 'page_id': 10, 'icon': 'settings'},
            {'name': 'Product', 'url': 'product-home', 'section': 'Product Data Management', 'page_id': 11, 'icon': 'shopping-bag'},
            {'name': 'Product Batch', 'url': 'product-batch-list', 'section': 'Product Data Management', 'page_id': 12, 'icon': 'shopping-cart'},
            
            # Miscellaneous Data Management
            {'name': 'Units', 'url': 'unit-list', 'section': 'Miscellaneous Data Management', 'page_id': 13, 'icon': 'hash'},
            {'name': 'Grade', 'url': 'grade-list', 'section': 'Miscellaneous Data Management', 'page_id': 14, 'icon': 'star'},
            {'name': 'Enduse', 'url': 'enduse-list', 'section': 'Miscellaneous Data Management', 'page_id': 15, 'icon': 'target'},
            {'name': 'Document Type', 'url': 'documenttype-list', 'section': 'Miscellaneous Data Management', 'page_id': 16, 'icon': 'file-text'},
            {'name': 'Center', 'url': 'center-list', 'section': 'Miscellaneous Data Management', 'page_id': 17, 'icon': 'map-pin'},
            {'name': 'Division', 'url': 'division-list', 'section': 'Miscellaneous Data Management', 'page_id': 18, 'icon': 'git-branch'},
            {'name': 'Source', 'url': 'source-list', 'section': 'Miscellaneous Data Management', 'page_id': 19, 'icon': 'external-link'},
            {'name': 'Supplier', 'url': 'supplier-list', 'section': 'Miscellaneous Data Management', 'page_id': 20, 'icon': 'truck'},
            
            # User Management
            {'name': 'Users', 'url': 'user-list', 'section': 'User Management', 'page_id': 21, 'icon': 'users'},
            
            # Report Generation
            {'name': 'Process Log-Sheet', 'url': '#', 'section': 'Report Generation', 'page_id': 22, 'icon': 'clipboard'},
            {'name': 'Stage Clearance', 'url': 'clearance', 'section': 'Report Generation', 'page_id': 23, 'icon': 'unlock'},
            {'name': 'Q.A.R-Report', 'url': '#', 'section': 'Report Generation', 'page_id': 24, 'icon': 'file-text'},
            
            # Roles Management
            {'name': 'Groups', 'url': 'group-list', 'section': 'Roles Management', 'page_id': 25, 'icon': 'users'},
        ]
        
        created_count = 0
        updated_count = 0
        
        for page_data in vssc_pages:
            page, created = Page.objects.update_or_create(
                page_id=page_data['page_id'],
                defaults={
                    'name': page_data['name'],
                    'url': page_data['url'],
                    'section': page_data['section'],
                    'icon': page_data['icon'],
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'Created page: {page.name}')
            else:
                updated_count += 1
                self.stdout.write(f'Updated page: {page.name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded VSSC pages! Created: {created_count}, Updated: {updated_count}'
            )
        )
