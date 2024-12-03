from django.db import models
from .grade import Grade
# from qdpc_core_models.models.user import User
from .source import Sources
from .supplier import Suppliers
from .acceptance_test import AcceptanceTest
from datetime import timedelta
from qdpc_core_models.models.document_categary import DocumentCategory




class RawMaterial(models.Model):
    name = models.CharField(max_length=255, unique=True)
    sources = models.ManyToManyField(Sources, related_name='raw_materials')
    is_active = models.BooleanField(default=True)
    precertified = models.BooleanField(default=False, blank=True, null=True)  
    suppliers = models.ManyToManyField(Suppliers, related_name='raw_materials')
    grade = models.ManyToManyField(Grade, related_name='raw_materials')
    shelf_life_value = models.FloatField()
    shelf_life_unit = models.CharField(max_length=10, choices=[('days', 'Days'), ('months', 'Months')])
    user_defined_date = models.DateField(auto_now_add=False,)
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
    
    raw_material = models.CharField(max_length=255,unique=True,null=True,blank=True)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORY_NAME_CHOICES, default='PDF')
    issue_no = models.CharField(max_length=255)
    revision_no = models.CharField(max_length=255)
    release_date = models.DateField()
    approved_by = models.CharField(max_length=255)
    document = models.FileField(upload_to='rawmaterial_documents')
    validity = models.IntegerField(help_text="Validity in years")

    def __str__(self):
        return f"{self.title} - {self.raw_material}"
