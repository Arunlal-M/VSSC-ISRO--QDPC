
from django.db import models
from qdpc_core_models.models.product_category import ProductCategory
from qdpc_core_models.models.division import Division
from qdpc_core_models.models.porcessing_agency import ProcessingAgency
from qdpc_core_models.models.product_component import ProductComponent
from qdpc_core_models.models.raw_material import RawMaterial
from qdpc_core_models.models.consumable import Consumable

from qdpc_core_models.models.enduse import EndUse
from qdpc_core_models.models.testing_agency import TestingAgency
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from qdpc_core_models.models.equipment import Equipment
from qdpc_core_models.models.document_type import DocumentType


class Product(models.Model):
    IDENTIFICATION_METHODS = [
        ('Batch Number', 'Product with batch no.'),
        ('Identification Number', 'Product with identification no.')
    ]
    
    SHELF_LIFE_OPTIONS = [
        ('tbd', 'TBD (To Be Decided)'),
        ('not_applicable', 'Not Applicable'),
        ('add_duration', 'Add Duration'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_owner = models.ForeignKey(Division, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)  # Active Status
    end_uses = models.ForeignKey(EndUse, on_delete=models.CASCADE,related_name='product_enduse',blank=True, null=True)
    specific_use = models.TextField(blank=True, null=True)
    shelf_life_type = models.CharField(max_length=20, choices=SHELF_LIFE_OPTIONS, null=True, blank=True, default='tbd',)
    shelf_life_value = models.FloatField(null=True, blank=True)
    shelf_life_unit = models.CharField(max_length=10, choices=[('days', 'Days'), ('months', 'Months')],null=True,blank=True)
    processing_agencies =  models.ForeignKey(Division, on_delete=models.CASCADE,related_name='products',blank=True, null=True)
    testing_agencies = models.ForeignKey(Division, on_delete=models.CASCADE,related_name='products_testingagency',blank=True, null=True)
    components = models.ManyToManyField(ProductComponent, blank=True)
    drawing_number = models.CharField(max_length=100, blank=True, null=True)
    drawing_status = models.CharField(max_length=50, choices=[('Provisional', 'Provisional'), ('CCB approved', 'CCB approved')], blank=True, null=True)
    identification_method = models.CharField(max_length=50, choices=IDENTIFICATION_METHODS)
    batch_size = models.TextField(blank=True, null=True)
    prefix = models.CharField(max_length=50, blank=True, null=True)
    suffix = models.CharField(max_length=50, blank=True, null=True)
    rawmaterial=models.ManyToManyField(RawMaterial,blank=True)
    consumable=models.ManyToManyField(Consumable,blank=True)
    equipment=models.ManyToManyField(Equipment,blank=True)
    drawing_applicable = models.CharField(max_length=3, choices=[("yes", "Yes"), ("no", "No")], default="no",blank=True, null=True)
    drawing_title = models.CharField(max_length=100, blank=True, null=True)
    drawing_document = models.FileField(upload_to='drawingfiles/', null=True, blank=True)
    product_document = models.BooleanField(default=False, blank=True, null=True)  
    # product_document = models.FileField(upload_to='productfiles/', null=True, blank=True)


    def __str__(self):
        return self.name

    def calculate_expiry_date(self, user_defined_date):
        if self.shelf_life_value and self.shelf_life_unit:
            if self.shelf_life_unit == 'days':
                return user_defined_date + timedelta(days=self.shelf_life_value)
            elif self.shelf_life_unit == 'months':
                return user_defined_date + relativedelta(months=self.shelf_life_value)
        return None
    
class ProductDocument(models.Model):
        
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
    
    product = models.CharField(max_length=255,unique=True,null=True,blank=True)
    title = models.CharField(max_length=255)
    document_category = models.ForeignKey(DocumentType, on_delete=models.CASCADE,related_name='product_documenttype',blank=True, null=True)
    issue_no = models.CharField(max_length=255)
    revision_no = models.CharField(max_length=255)
    release_date = models.DateField()
    approved_by = models.CharField(max_length=255)
    document = models.FileField(upload_to='productfiles/')
    validity = models.IntegerField(help_text="Validity in years")

    def __str__(self):
        return f"{self.title} - {self.product}"    
    