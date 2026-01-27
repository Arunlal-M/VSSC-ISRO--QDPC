from django.db import models
from django.utils import timezone
from datetime import timedelta
from qdpc_core_models.models.raw_materialbach import RawMaterialBatch
from qdpc_core_models.models.consumablebatch import ConsumableBatch
from qdpc_core_models.models.componentbatch import ComponentBatch
from qdpc_core_models.models.process import Process
from qdpc_core_models.models.product import Product
from qdpc_core_models.models.unit import Unit
from qdpc_core_models.models.user import User

class ProductBatch(models.Model):
    STATUS_CHOICES = [  
        ('pending', 'Pending QA'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
    ]
    
    # ... (your existing fields) ...
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'  # Default status is now 'pending'
    )
    batch_id = models.CharField(max_length=100, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    manufacturings_start_date = models.DateField()
    manufacturings_end_date = models.DateField()
    raw_material_batch = models.ForeignKey(RawMaterialBatch, on_delete=models.CASCADE)
    consumable_batch = models.ForeignKey(ConsumableBatch, on_delete=models.CASCADE)
    component_batch = models.ForeignKey(ComponentBatch, on_delete=models.CASCADE)
    Process = models.ForeignKey(Process, on_delete=models.CASCADE)
    batch_size_value = models.FloatField()
    batch_size_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='product_batch_sizes')
    packing_details = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # User who created the record
    qa_approval_date = models.DateTimeField(null=True, blank=True)
    dynamic_tables_data = models.TextField(null=True, blank=True)
    qa_approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_product_batches'
    )
    rejection_reason = models.TextField(null=True, blank=True)


    def submit_for_qa(self):
        """Mark batch as pending QA (this is now the default status)"""
        self.status = 'pending'
        self.save()
        return True

    def approve(self, user):
        """Approve the batch and make it active"""
        if self.status == 'pending':
            self.status = 'active'  # Changed from 'approved' to 'active'
            self.qa_approval_date = timezone.now()
            self.qa_approved_by = user
            self.rejection_reason = None
            self.save()
            return True
        return False

    def reject(self, user, reason):
        """Reject the batch"""
        if self.status == 'pending':
            self.status = 'rejected'
            self.rejection_reason = reason
            self.save()
            return True
        return False

    class Meta:
        permissions = [
            ("can_approve_productbatch", "Can approve product batches"),
            ("can_reject_productbatch", "Can reject product batches"),
        ]
    def __str__(self):
        return self.batch_id