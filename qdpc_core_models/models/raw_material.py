from django.db import models
from .grade import Grade
# from qdpc_core_models.models.user import User
from .source import Sources
from .supplier import Suppliers
from .acceptance_test import AcceptanceTest
from datetime import timedelta
from django.utils.timezone import now
from qdpc_core_models.models.document_categary import DocumentCategory
from qdpc_core_models.models.document_type import DocumentType

class RawMaterial(models.Model):
    
    SHELF_LIFE_OPTIONS = [
        ('tbd', 'TBD (To Be Decided)'),
        ('not_applicable', 'Not Applicable'),
        ('add_duration', 'Add Duration'),
    ]
        
    name = models.CharField(max_length=255, unique=True)
    sources = models.ManyToManyField(Sources, related_name='raw_materials')
    is_active = models.BooleanField(default=True)
    precertified = models.BooleanField(default=False, blank=True, null=True)  
    suppliers = models.ManyToManyField(Suppliers, related_name='raw_materials')
    grade = models.ManyToManyField(Grade, related_name='raw_materials')
    shelf_life_type = models.CharField(max_length=20, choices=SHELF_LIFE_OPTIONS, null=True, blank=True, default='tbd',)
    shelf_life_value = models.FloatField(null=True, blank=True)
    shelf_life_unit = models.CharField(max_length=10, choices=[('days', 'Days'), ('months', 'Months')],null=True,blank=True)
    user_defined_date = models.DateField(default=now)
    acceptance_test = models.ManyToManyField(AcceptanceTest, blank=True, null=True, related_name='raw_materials')

    @property
    def calculate_expiry_date(self):
        procurement_date = self.user_defined_date
        if self.shelf_life_unit == 'days':
            return procurement_date + timedelta(days=self.shelf_life_value)
        elif self.shelf_life_unit == 'months':
            return procurement_date + timedelta(days=self.shelf_life_value * 30)  # Approximation for months

    def __str__(self):
        return self.name


class RawMaterialDocument(models.Model):
        
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
    
    raw_material = models.CharField(max_length=255,unique=True,null=True,blank=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(DocumentType, on_delete=models.CASCADE,related_name='rawmaterial_documenttype',blank=True, null=True)
    issue_no = models.CharField(max_length=255)
    revision_no = models.CharField(max_length=255)
    release_date = models.DateField()
    approved_by = models.CharField(max_length=255)
    document = models.FileField(upload_to='rawmaterial_documents')
    validity = models.IntegerField(help_text="Validity in years")

    def __str__(self):
        return f"{self.title} - {self.raw_material}"
