# equipment/forms.py

from django import forms
# from .models import Equipment
from qdpc_core_models.models.equipment import Equipment,EquipmentDocument



class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'serial_no', 'make', 'last_calibration_date', 
                  'calibration_validity_duration_type', 'calibration_validity_duration_value']

class EquipmentDocumentForm(forms.ModelForm):
    class Meta:
        model = EquipmentDocument
        fields = ['title', 'release_date', 'approved_by', 'documentfile']

