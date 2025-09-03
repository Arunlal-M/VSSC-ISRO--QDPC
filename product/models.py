from django.db import models
from qdpc_core_models.models.productBatch import *
from qdpc_core_models.models.product_batchlist import ProductBatch

# Create your models here.

class DynamicTable(models.Model):
    product_batch = models.ForeignKey(ProductBatchs, related_name='tables', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    columns = models.JSONField(default=list)

    def __str__(self):
        return f"{self.title} ({self.product_batch.name})"

class DynamicTableRow(models.Model):
    table = models.ForeignKey(DynamicTable, related_name='rows', on_delete=models.CASCADE)
    data = models.JSONField()  # Stores each row as a dictionary: {"0": "value1", "1": "value2"}

    def __str__(self):
        return f"Row in {self.table.title}"