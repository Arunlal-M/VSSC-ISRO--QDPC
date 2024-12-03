from django.db import models
from qdpc_core_models.models.consumable import Consumable
from qdpc_core_models.models.document_categary import DocumentCategory


class ConsumableDocument(models.Model):
    
    CATEGORY_NAME_CHOICES = [
        ('DOC/DOCX', '.doc/.docx'),
        ('PDF', '.pdf'),
        ('TXT', '.txt'),
        ('XLS/XLSX', '.xls/.xlsx'),
        ('CSV', '.csv'),
        ('PPT/PPTX', '.ppt/.pptx'),
        ('ODP', '.odp'),
        ('JPG/JPEG', '.jpg/.jpeg'),
        ('PNG', '.png'),
        ('ZIP', '.zip'),
        ('RAR', '.rar'),
     ]
    
    consumable = models.ForeignKey(Consumable, on_delete=models.CASCADE, related_name='consumable_documents')
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORY_NAME_CHOICES, default='PDF')
    issue_no = models.CharField(max_length=255)
    revision_no = models.CharField(max_length=255)
    release_date = models.DateField()
    approved_by = models.CharField(max_length=255)
    document = models.FileField(upload_to='consumable_document/')
    validity = models.IntegerField(help_text="Validity in years")

    def __str__(self):
        return f"{self.title} - {self.category} - {self.consumable.name}"
