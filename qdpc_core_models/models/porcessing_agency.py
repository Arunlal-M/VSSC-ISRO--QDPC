from django.db import models
class ProcessingAgency(models.Model):
    AGENCY_TYPES = [
        ('In-house', 'In-house'),
        ('Industry', 'Industry'),
        ('GOCO', 'GOCO'),
        ('In-house + GOCO', 'In-house + GOCO'),
        ('In-house + Industry', 'In-house + Industry'),
        ('In-house + GOCO + Industry', 'In-house + GOCO + Industry'),
        ('GOCO + Industry', 'GOCO + Industry'),
    ]
    name = models.CharField(max_length=100)
    agency_type = models.CharField(max_length=50, choices=AGENCY_TYPES)

    def __str__(self):
        return f"{self.name} ({self.agency_type})"