from django.db import models
from qdpc_core_models.models.acceptance_test import AcceptanceTest

class TestResult(models.Model):
    acceptance_test = models.ForeignKey(AcceptanceTest, on_delete=models.CASCADE, related_name='test_results')
    result_file = models.FileField(upload_to='acceptance_test_results/')  # To store PDF or image files
    test_date = models.DateField()
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.acceptance_test.name} - {self.test_date}"
