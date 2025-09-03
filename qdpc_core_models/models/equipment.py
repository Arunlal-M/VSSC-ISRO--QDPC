from django.db import models
from datetime import timedelta
from .division import Division
from qdpc_core_models.models.document_type import DocumentType
from django.utils.timezone import now
from datetime import timedelta


class Equipment(models.Model):
    CALIBRATION_VALIDITY_CHOICES = [
        ('days', 'Days'),
        ('months', 'Months'),
        ('years', 'Years'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150,unique=True)
    serial_no = models.CharField(max_length=150, unique=True)
    make = models.CharField(max_length=255)
    last_calibration_date = models.DateField()
    calibration_validity_duration_type = models.CharField( max_length=6,choices=CALIBRATION_VALIDITY_CHOICES,)
    calibration_validity_duration_value = models.IntegerField()
    calibration_due_date = models.DateField(editable=False)
    calibration_certificate = models.CharField(max_length=255, blank=True, null=True)
    equipment_owner=models.ForeignKey(Division,on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 


    def save(self, *args, **kwargs):
        # Calculate calibration due date based on last calibration date and validity duration
        if self.calibration_validity_duration_type == 'days':
            self.calibration_due_date = self.last_calibration_date + timedelta(days=self.calibration_validity_duration_value)
        elif self.calibration_validity_duration_type == 'months':
            self.calibration_due_date = self.last_calibration_date + timedelta(days=self.calibration_validity_duration_value * 30)
        elif self.calibration_validity_duration_type == 'years':
            self.calibration_due_date = self.last_calibration_date + timedelta(days=self.calibration_validity_duration_value * 365)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.serial_no})"
    
class EquipmentDocument(models.Model):    
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    approved_by = models.CharField(max_length=255)
    documentfile = models.FileField(upload_to='calibration_certificates/')

    def __str__(self):
        return f"{self.title} - {self.equipment}"

