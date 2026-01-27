from django.db import models
from .grade import Grade
# from qdpc_core_models.models.user import User
from .source import Sources
from .supplier import Suppliers
from .acceptance_test import AcceptanceTest
from datetime import timedelta
from django.utils.timezone import now
from qdpc_core_models.models.document_type import DocumentType


class Component(models.Model):
    
    SHELF_LIFE_OPTIONS = [
        ('tbd', 'TBD (To Be Decided)'),
        ('not_applicable', 'Not Applicable'),
        ('add_duration', 'Add Duration'),
    ]
    name = models.CharField(max_length=150,unique=True)
    sources = models.ManyToManyField(Sources, related_name='components')
    is_active = models.BooleanField(default=True)  # Active Status
    precertified = models.BooleanField(default=False, blank=True, null=True)
    suppliers = models.ManyToManyField(Suppliers, related_name='components')
    # grade = models.CharField(max_length=50)
    grade = models.ManyToManyField(Grade, related_name='components')
    shelf_life_type = models.CharField(max_length=20, choices=SHELF_LIFE_OPTIONS, null=True, blank=True, default='tbd',)
    shelf_life_value = models.FloatField(null=True, blank=True)
    shelf_life_unit = models.CharField(max_length=10, choices=[('days', 'Days'), ('months', 'Months'),('years', 'Years')],null=True,blank=True)
    user_defined_date = models.DateField(default=now)
    acceptance_test = models.ManyToManyField(AcceptanceTest,blank=True, related_name='components')
    created_at = models.DateTimeField(auto_now_add=True) 

    @property
    def calculate_expiry_date(self):
        # Check if we have valid shelf life data
        if not self.shelf_life_value or not self.shelf_life_unit:
            return None
            
        # Use current date as base for calculation if no user_defined_date
        base_date = self.user_defined_date if self.user_defined_date else now().date()
        
        try:
            if self.shelf_life_unit == 'days':
                return base_date + timedelta(days=self.shelf_life_value)
            elif self.shelf_life_unit == 'months':
                return base_date + timedelta(days=self.shelf_life_value * 30)  # Approximation for months
            elif self.shelf_life_unit == 'years':
                return base_date + timedelta(days=self.shelf_life_value * 365)  # Approximation for years
            else:
                return None  # Handle cases where shelf_life_unit is not set or invalid
        except (TypeError, ValueError):
            # Handle any calculation errors gracefully
            return None
        
    def __str__(self):
        return self.name


class ComponentDocument(models.Model):  
    component = models.CharField(max_length=150,unique=True,null=True,blank=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(DocumentType, on_delete=models.CASCADE,related_name='component_documenttype',blank=True, null=True)
    issue_no = models.CharField(max_length=255)
    revision_no = models.CharField(max_length=255)
    release_date = models.DateField()
    approved_by = models.CharField(max_length=255)
    document = models.FileField(upload_to='component_documents')
    validity = models.IntegerField(help_text="Validity in years")

    def __str__(self):
        return f"{self.title} - {self.component}"
