from django.core.management.base import BaseCommand
from qdpc_core_models.models.process import Process, ProcessStep
from qdpc_core_models.models.product import Product
from qdpc_core_models.models.productBatch import ProductBatchs, ProductBatchProcess


class Command(BaseCommand):
    help = 'Check and debug process data in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-sample',
            action='store_true',
            help='Create sample process data if none exists',
        )

    def handle(self, *args, **options):
        self.stdout.write("=== PROCESS DATA DEBUG REPORT ===")
        
        # Check total processes
        total_processes = Process.objects.count()
        self.stdout.write(f"Total processes in system: {total_processes}")
        
        if total_processes == 0:
            self.stdout.write(self.style.WARNING("No processes found in database!"))
            if options['create_sample']:
                self.create_sample_processes()
        else:
            # List all processes
            for process in Process.objects.all():
                steps_count = ProcessStep.objects.filter(process=process).count()
                self.stdout.write(f"Process: '{process.process_title}' (ID: {process.id}) - {steps_count} steps")
                
                if steps_count > 0:
                    for step in ProcessStep.objects.filter(process=process).order_by('step_id'):
                        self.stdout.write(f"  - Step {step.step_id}: {step.process_description}")
                else:
                    self.stdout.write(f"  - No steps found for this process")
        
        # Check product batches and their processes
        self.stdout.write("\n=== PRODUCT BATCH PROCESS CHECK ===")
        total_batches = ProductBatchs.objects.count()
        self.stdout.write(f"Total product batches: {total_batches}")
        
        for batch in ProductBatchs.objects.all()[:5]:  # Check first 5 batches
            batch_processes = ProductBatchProcess.objects.filter(product_batch=batch)
            self.stdout.write(f"Batch {batch.batch_id} (ID: {batch.id}): {batch_processes.count()} processes")
            
            for bp in batch_processes:
                process = bp.process
                steps = ProcessStep.objects.filter(process=process)
                self.stdout.write(f"  - Process: {process.process_title} - {steps.count()} steps")
        
        # Check products and their processes
        self.stdout.write("\n=== PRODUCT PROCESS CHECK ===")
        products_with_processes = Product.objects.filter(process__isnull=False).distinct()
        self.stdout.write(f"Products with processes: {products_with_processes.count()}")
        
        for product in products_with_processes[:5]:  # Check first 5 products
            processes = product.process.all()
            self.stdout.write(f"Product '{product.name}' (ID: {product.id}): {processes.count()} processes")
            
            for process in processes:
                steps = ProcessStep.objects.filter(process=process)
                self.stdout.write(f"  - Process: {process.process_title} - {steps.count()} steps")

    def create_sample_processes(self):
        """Create sample process data for testing"""
        self.stdout.write("Creating sample process data...")
        
        # Create a sample process
        process1 = Process.objects.create(
            process_title="Sample Manufacturing Process",
            description="A sample manufacturing process for testing"
        )
        
        # Create process steps
        ProcessStep.objects.create(
            process=process1,
            step_id=1,
            process_description="Raw Material Preparation",
            process_date="2024-01-01",
            rm_status="Ready",
            equipment_status="Ready",
            consumable_status="Ready",
            component_status="Ready",
            remarks="Prepare raw materials for processing",
            test_result="PASS",
            specification_result="PASS"
        )
        
        ProcessStep.objects.create(
            process=process1,
            step_id=2,
            process_description="Initial Processing",
            process_date="2024-01-01",
            rm_status="In Progress",
            equipment_status="In Use",
            consumable_status="In Use",
            component_status="Ready",
            remarks="Begin initial processing phase",
            test_result="PASS",
            specification_result="PASS"
        )
        
        ProcessStep.objects.create(
            process=process1,
            step_id=3,
            process_description="Quality Check",
            process_date="2024-01-01",
            rm_status="Complete",
            equipment_status="Complete",
            consumable_status="Complete",
            component_status="Complete",
            remarks="Final quality check before completion",
            test_result="PASS",
            specification_result="PASS"
        )
        
        self.stdout.write(self.style.SUCCESS("Sample process data created successfully!"))
        self.stdout.write(f"Created process: {process1.process_title} with 3 steps")
