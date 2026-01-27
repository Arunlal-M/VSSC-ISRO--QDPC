from django.db import models
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.component import Component
from qdpc_core_models.models.source import Sources
from qdpc_core_models.models.supplier import Suppliers
from qdpc_core_models.models.grade import Grade
from qdpc_core_models.models.user import User
from qdpc_core_models.models.component import Component



class ComponentAcceptanceTest(models.Model):
    # created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # User who created the record

    id = models.AutoField(primary_key=True)
    batch_id = models.CharField(max_length=255)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='component_acceptance_tests')
    component_unit = models.CharField(max_length=255)  # <-- Add this line
    acceptance_test = models.ForeignKey(AcceptanceTest, on_delete=models.CASCADE)
    test_value = models.CharField(max_length=255,blank=True,null=True)
    sources = models.ForeignKey(Sources, on_delete=models.CASCADE)
    suppliers = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    min_value = models.IntegerField(blank=True, null=True)  # Add min_value field
    max_value = models.IntegerField(blank=True, null=True)  # Add max_value field
    file = models.FileField(upload_to='component_acceptance_tests/')
    created_by = models.CharField(max_length=255)
    status = models.CharField(max_length=255,blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.component.name}"
