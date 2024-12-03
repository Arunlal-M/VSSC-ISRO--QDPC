from django.db import models

class TestingAgency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    # processing_agency=
        

    def __str__(self):
        return self.name