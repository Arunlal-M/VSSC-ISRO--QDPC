from django.db import models
from qdpc_core_models.models.raw_materialbach import RawMaterialBatch
from qdpc_core_models.models.consumablebatch import ConsumableBatch
from qdpc_core_models.models.componentbatch import ComponentBatch
from qdpc_core_models.models.equipment import Equipment
from qdpc_core_models.models.unit import Unit

class Process(models.Model):
    id = models.AutoField(primary_key=True)
    process_title = models.CharField(max_length=255)    
    
    def __str__(self):
        return self.process_title

class ProcessStep(models.Model):
    
    PROCESS_TYPE_CHOICES = [
        ('quantitative', 'Quantitative'),
        ('qualitative', 'Qualitative'),
    ]
    # id = models.AutoField(primary_key=True)
    process = models.ForeignKey(Process, related_name='process', on_delete=models.CASCADE)
    step_id = models.PositiveIntegerField()  # Manually managed field
    raw_material_batch = models.ManyToManyField(RawMaterialBatch, related_name='process_steps')
    consumable_batch = models.ManyToManyField(ConsumableBatch, related_name='process_steps')
    component_batch = models.ManyToManyField(ComponentBatch, related_name='process_steps')
    equipment = models.ManyToManyField(Equipment, related_name='process_steps')
    process_description = models.TextField(null=True, blank=True)
    process_date = models.DateField()
    min_value = models.IntegerField(blank=True, null=True)  # Optional field
    max_value = models.IntegerField(blank=True, null=True) 
    unit = models.ManyToManyField(Unit, related_name='process_steps')
    test_result = models.CharField(max_length=10, blank=True, null=True)
    specification_result = models.CharField(max_length=10, blank=True, null=True)
    process_type = models.CharField(max_length=15, choices=PROCESS_TYPE_CHOICES, default='quantitateive')


    rm_status = models.CharField(max_length=50, choices=[
        ('Material Valid', 'Material Valid'),
        ('Material Expired', 'Material Expired'),
    ])
    
    equipment_status = models.CharField(max_length=50, choices=[
        ('Calibration Valid', 'Calibration Valid'),
        ('Calibration Expired', 'Calibration Expired'),
    ])
    consumable_status = models.CharField(max_length=50, choices=[
        ('Consumable Valid', 'Consumable Valid'),
        ('Consumable Expired', 'Consumable Expired'),
    ])
    component_status = models.CharField(max_length=50, choices=[
        ('Component Valid', 'Component Valid'),
        ('Component Expired', 'Component Expired'),
    ])
    
    # process_step_spec = models.TextField()
    # measured_value_observation = models.TextField()
    remarks = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.step_id:
            # Assign the next step ID based on the existing steps for this process
            last_step = ProcessStep.objects.filter(process=self.process).order_by('step_id').last()
            self.step_id = last_step.step_id + 1 if last_step else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Step {self.step_id} of {self.process.process_title}"