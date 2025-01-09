
from django.db import models

class DocumentCategory(models.Model):
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
    name = models.CharField(max_length=255, choices=CATEGORY_NAME_CHOICES, unique=True, default='PDF')

    def __str__(self):
        return self.name