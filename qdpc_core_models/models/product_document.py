from django.db import models

from qdpc_core_models.models.product import Product

class Document(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    issue_no = models.CharField(max_length=50)
    revision_no = models.CharField(max_length=50, unique=True)
    release_date = models.DateField()
    approved_by = models.CharField(max_length=100)
    document_file = models.FileField(upload_to='documents/')
    validity_in_years = models.IntegerField()

    def __str__(self):
        return f"{self.title} ({self.product.name})"