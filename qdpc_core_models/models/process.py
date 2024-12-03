from django.db import models
from qdpc_core_models.models.raw_material import RawMaterial
from qdpc_core_models.models.consumable import Consumable
from qdpc_core_models.models.component import Component
from qdpc_core_models.models.equipment import Equipment

class Process(models.Model):
    
    process_title = models.CharField(max_length=255, primary_key=True)
    

    def __str__(self):
        return self.process_title


class ProcessStep(models.Model):
    process = models.ForeignKey(Process, related_name='process', on_delete=models.CASCADE)
    step_id = models.PositiveIntegerField()  # Manually managed field
    raw_material = models.ManyToManyField(RawMaterial, related_name='process_steps')
    consumable = models.ManyToManyField(Consumable, related_name='process_steps')
    component = models.ManyToManyField(Component, related_name='process_steps')
    equipment = models.ManyToManyField(Equipment, related_name='process_steps')
    process_description = models.TextField(null=True, blank=True)
    process_date = models.DateField()

    rm_status = models.CharField(max_length=50, choices=[
        ('Valid', 'Valid'),
        ('Material Expired', 'Material Expired'),
        ('Test Certificate Expired', 'Test Certificate Expired'),
    ])
    
    equipment_status = models.CharField(max_length=50, choices=[
        ('Calibration Valid', 'Calibration Valid'),
        ('Calibration Expired', 'Calibration Expired'),
    ])
    
    process_step_spec = models.TextField()
    measured_value_observation = models.TextField()
    remarks = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.step_id:
            # Assign the next step ID based on the existing steps for this process
            last_step = ProcessStep.objects.filter(process=self.process).order_by('step_id').last()
            self.step_id = last_step.step_id + 1 if last_step else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Step {self.step_id} of {self.process.process_title}"