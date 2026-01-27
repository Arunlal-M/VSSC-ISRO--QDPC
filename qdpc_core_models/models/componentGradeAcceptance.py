from django.db import models
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.component import Component
from qdpc_core_models.models.source import Sources
from qdpc_core_models.models.supplier import Suppliers
from qdpc_core_models.models.grade import Grade
from qdpc_core_models.models.user import User



class ComponentGradeAcceptanceTest(models.Model):
    # created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # User who created the record

    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='test_data')
    acceptance_test = models.ForeignKey(AcceptanceTest, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    min_value = models.FloatField()
    max_value = models.FloatField()
    unit_name = models.CharField(max_length=20)
    reevaluation_frequency = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.component.name}"
