from django.db import models
from datetime import timedelta
from .division import Division
from qdpc_core_models.models.document_type import DocumentType


class Equipment(models.Model):
    CALIBRATION_VALIDITY_CHOICES = [
        ('days', 'Days'),
        ('months', 'Months'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    serial_no = models.CharField(max_length=255, unique=True)
    make = models.CharField(max_length=255)
    last_calibration_date = models.DateField()
    calibration_validity_duration_type = models.CharField( max_length=6,choices=CALIBRATION_VALIDITY_CHOICES,)
    calibration_validity_duration_value = models.IntegerField()
    calibration_due_date = models.DateField(editable=False)
    calibration_certificate = models.CharField(max_length=255, blank=True, null=True)
    equipment_owner=models.ForeignKey(Division,on_delete=models.CASCADE,null=True, blank=True)


    def save(self, *args, **kwargs):
        # Calculate calibration due date based on last calibration date and validity duration
        if self.calibration_validity_duration_type == 'days':
            self.calibration_due_date = self.last_calibration_date + timedelta(days=self.calibration_validity_duration_value)
        elif self.calibration_validity_duration_type == 'months':
            self.calibration_due_date = self.last_calibration_date + timedelta(days=self.calibration_validity_duration_value * 30)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.serial_no})"
    
    
class EquipmentDocument(models.Model):
        
    # CATEGORY_NAME_CHOICES = [
    #     ('DOC/DOCX', '.doc/.docx'),
    #     ('PDF', '.pdf'),
    #     ('TXT', '.txt'),
    #     ('XLS/XLSX', '.xls/.xlsx'),
    #     ('CSV', '.csv'),
    #     ('PPT/PPTX', '.ppt/.pptx'),
    #     ('ODP', '.odp'),
    #     ('JPG/JPEG', '.jpg/.jpeg'),
    #     ('PNG', '.png'),
    #     ('ZIP', '.zip'),
    #     ('RAR', '.rar'),
    #  ]
    
    equipment = models.CharField(max_length=255,unique=True,null=True,blank=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(DocumentType, on_delete=models.CASCADE,related_name='equipment_documenttype',blank=True, null=True)
    issue_no = models.CharField(max_length=255)
    revision_no = models.CharField(max_length=255)
    release_date = models.DateField()
    approved_by = models.CharField(max_length=255)
    document = models.FileField(upload_to='calibration_certificates/')
    validity = models.IntegerField(help_text="Validity in years")

    def __str__(self):
        return f"{self.title} - {self.equipment}"
