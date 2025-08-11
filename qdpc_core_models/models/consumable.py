from django.db import models
from .grade import Grade
# from qdpc_core_models.models.user import User
from .source import Sources
from .supplier import Suppliers
from .acceptance_test import AcceptanceTest
from datetime import timedelta
from django.utils.timezone import now
from qdpc_core_models.models.document_type import DocumentType
from qdpc_core_models.models.division import Division
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



class Consumable(models.Model):
    
    SHELF_LIFE_OPTIONS = [
        ('tbd', 'TBD (To Be Decided)'),
        ('not_applicable', 'Not Applicable'),
        ('add_duration', 'Add Duration'),
    ]
    
    name = models.CharField(max_length=150,unique=True)
    sources = models.ManyToManyField(Sources, related_name='consumables')
    is_active = models.BooleanField(default=True)  # Active Status
    precertified = models.BooleanField(default=False, blank=True, null=True)  
    document_upload = models.BooleanField(default=False, blank=True, null=True)  
    suppliers = models.ManyToManyField(Suppliers, related_name='consumables')
    # grade = models.CharField(max_length=50)
    grade = models.ManyToManyField(Grade, related_name='consumables')
    shelf_life_type = models.CharField(max_length=20, choices=SHELF_LIFE_OPTIONS, null=True, blank=True, default='tbd',)
    shelf_life_value = models.FloatField(null=True, blank=True)
    shelf_life_unit = models.CharField(max_length=10, choices=[('days', 'Days'), ('months', 'Months'),('years', 'Years')],null=True,blank=True)
    user_defined_date = models.DateField(default=now)
    acceptance_test = models.ManyToManyField(AcceptanceTest, blank=True, related_name='consumables')
    created_at = models.DateTimeField(auto_now_add=True) 

    @property
    def calculate_expiry_date(self):
        procurement_date = self.user_defined_date  # Use user_defined_date as the default procurement_date
        if self.shelf_life_unit == 'days':
            return procurement_date + timedelta(days=self.shelf_life_value)
        elif self.shelf_life_unit == 'months':
            return procurement_date + timedelta(days=self.shelf_life_value * 30)  # Approximation for months
        elif self.shelf_life_unit == 'years':
             return procurement_date + timedelta(days=self.shelf_life_value * 365)  # Approximation for years
        return None  # Handle cases where shelf_life_unit is not set or invalid
        

    def __str__(self):
        return self.name
    
class ConsumableDocument(models.Model):
        
    consumable = models.CharField(max_length=150,unique=True,null=True,blank=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(DocumentType, on_delete=models.CASCADE,related_name='consumable_documenttype',blank=True, null=True)
    issue_no = models.CharField(max_length=255)
    revision_no = models.CharField(max_length=255)
    release_date = models.DateField()
    approved_by = models.CharField(max_length=255)
    document = models.FileField(upload_to='consumable_document')
    validity = models.IntegerField(help_text="Validity in years")

    def __str__(self):
        return f"{self.title} - {self.consumable}"
    

    
class PreCertification(models.Model):
    DISPOSITION_CHOICES = [
        ('CLEARED', 'Cleared for use'),
        ('PENDING', 'Cleared for use subject to completion of pending action'),
        ('NOT_CLEARED', 'Not Cleared'),
        ('OTHER', 'Other remarks'),
    ]

    # Generic relation fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    raw_material = GenericForeignKey('content_type', 'object_id')

    certified_by = models.ForeignKey(Division, on_delete=models.CASCADE)
    certificate_reference_no = models.CharField(max_length=100)
    certificate_issue_date = models.DateField()
    certificate_valid_till = models.DateField()
    certificate_file = models.FileField(upload_to='certificates/')
    certificate_disposition = models.CharField(max_length=20, choices=DISPOSITION_CHOICES)

    def __str__(self):
        return f"{self.raw_material} Certification"


class PendingAction(models.Model):
    certification = models.ForeignKey(PreCertification, on_delete=models.CASCADE, related_name='pending_actions')
    action_detail = models.TextField()

    def __str__(self):
        return f"Pending Action: {self.action_detail[:30]}"

class OtherRemark(models.Model):
    certification = models.ForeignKey(PreCertification, on_delete=models.CASCADE, related_name='other_remarks')
    remark_detail = models.TextField()

    def __str__(self):
        return f"Other Remark: {self.remark_detail[:30]}"