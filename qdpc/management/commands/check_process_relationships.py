from django.core.management.base import BaseCommand
from qdpc_core_models.models.process import Process, ProcessStep
from qdpc_core_models.models.consumablebatch import ConsumableBatch
from qdpc_core_models.models.componentbatch import ComponentBatch


class Command(BaseCommand):
    help = 'Check process step relationships and data for consumables and components'

    def add_arguments(self, parser):
        parser.add_argument(
            '--process-title',
            type=str,
            help='Check specific process by title',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Checking Process Step Relationships...'))
        
        if options['process_title']:
            processes = Process.objects.filter(process_title=options['process_title'])
        else:
            processes = Process.objects.all()
        
        for process in processes:
            self.stdout.write(f"\n{'='*60}")
            self.stdout.write(f"Process: {process.process_title}")
            self.stdout.write(f"{'='*60}")
            
            steps = ProcessStep.objects.filter(process=process).prefetch_related(
                'raw_material_batch',
                'consumable_batch',
                'component_batch',
                'equipment'
            )
            
            if not steps.exists():
                self.stdout.write(self.style.WARNING("  No process steps found"))
                continue
            
            for step in steps:
                self.stdout.write(f"\n  Step {step.step_id}: {step.process_description}")
                self.stdout.write(f"    Date: {step.process_date}")
                self.stdout.write(f"    Type: {step.process_type}")
                
                # Check Raw Materials
                raw_materials = list(step.raw_material_batch.all())
                if raw_materials:
                    self.stdout.write(f"    Raw Materials ({len(raw_materials)}):")
                    for rm in raw_materials:
                        self.stdout.write(f"      - {rm.name} (ID: {rm.id})")
                else:
                    self.stdout.write("    Raw Materials: None")
                
                # Check Consumables
                consumables = list(step.consumable_batch.all())
                if consumables:
                    self.stdout.write(f"    Consumables ({len(consumables)}):")
                    for cons in consumables:
                        self.stdout.write(f"      - {cons.name} (ID: {cons.id})")
                else:
                    self.stdout.write("    Consumables: None")
                
                # Check Components
                components = list(step.component_batch.all())
                if components:
                    self.stdout.write(f"    Components ({len(components)}):")
                    for comp in components:
                        self.stdout.write(f"      - {comp.name} (ID: {comp.id})")
                else:
                    self.stdout.write("    Components: None")
                
                # Check Equipment
                equipment = list(step.equipment.all())
                if equipment:
                    self.stdout.write(f"    Equipment ({len(equipment)}):")
                    for eq in equipment:
                        self.stdout.write(f"      - {eq.name} (ID: {eq.id})")
                else:
                    self.stdout.write("    Equipment: None")
                
                # Check Statuses
                self.stdout.write(f"    RM Status: {step.rm_status}")
                self.stdout.write(f"    Equipment Status: {step.equipment_status}")
                self.stdout.write(f"    Consumable Status: {step.consumable_status}")
                self.stdout.write(f"    Component Status: {step.component_status}")
        
        # Also check if there are any consumable or component batches in the system
        self.stdout.write(f"\n{'='*60}")
        self.stdout.write("Checking Available Data:")
        self.stdout.write(f"{'='*60}")
        
        consumable_count = ConsumableBatch.objects.count()
        component_count = ComponentBatch.objects.count()
        
        self.stdout.write(f"Total ConsumableBatches: {consumable_count}")
        self.stdout.write(f"Total ComponentBatches: {component_count}")
        
        if consumable_count > 0:
            self.stdout.write("Sample ConsumableBatches:")
            for cons in ConsumableBatch.objects.all()[:5]:
                self.stdout.write(f"  - {cons.name} (ID: {cons.id})")
        
        if component_count > 0:
            self.stdout.write("Sample ComponentBatches:")
            for comp in ComponentBatch.objects.all()[:5]:
                self.stdout.write(f"  - {comp.name} (ID: {comp.id})")
        
        self.stdout.write(self.style.SUCCESS('\nCheck completed!'))
