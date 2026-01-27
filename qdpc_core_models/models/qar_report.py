from django.db import models
from django.utils import timezone
from qdpc_core_models.models.productBatch import ProductBatchs
from qdpc_core_models.models.user import User

class QARReport(models.Model):
    """Model to store QAR (Quality Assessment Report) data with editable fields"""
    
    product_batch = models.ForeignKey(ProductBatchs, on_delete=models.CASCADE, related_name='qar_reports')
    
    # Report Header Information
    report_number = models.CharField(max_length=100, default='VSSC/QPDC/QAR/Product-A/2024/Rec: 2451')
    report_date = models.DateField(default=timezone.now)
    
    # Introduction Section
    introduction = models.TextField(blank=True, null=True, help_text="Brief introduction about the product and purpose of this report")
    scope = models.TextField(blank=True, null=True, help_text="Scope of the quality assessment")
    batch_summary = models.TextField(blank=True, null=True, help_text="Summary of the batches/units covered in this report")
    
    # End Use and Processing Agency
    end_use = models.TextField(blank=True, null=True, help_text="End use description")
    processing_agency = models.TextField(blank=True, null=True, help_text="Processing agency details")
    
    # Changes Section
    process_changes = models.TextField(blank=True, null=True, help_text="Summary of any changes in process, materials, or specifications")
    impact_assessment = models.TextField(blank=True, null=True, help_text="Impact assessment of changes")
    
    # QA Observations and Remarks
    raw_materials_qa = models.TextField(blank=True, null=True, help_text="QA observations and remarks for raw materials")
    components_qa = models.TextField(blank=True, null=True, help_text="QA observations and remarks for components")
    in_process_qa = models.TextField(blank=True, null=True, help_text="QA observations and remarks for in-process checks")
    inspections_qa = models.TextField(blank=True, null=True, help_text="QA observations and remarks for inspections")
    
    # Test Results and Quality Assurance
    test_results = models.TextField(blank=True, null=True, help_text="Summary of test results and findings")
    quality_assurance = models.TextField(blank=True, null=True, help_text="Quality assurance observations and recommendations")
    conclusion = models.TextField(blank=True, null=True, help_text="Overall conclusion and recommendations")
    
    # Additional Remarks
    additional_remarks = models.TextField(blank=True, null=True, help_text="Any additional remarks or notes")
    
    # Report Personnel
    engineer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='engineer_qar_reports', help_text="Engineer responsible for the report")
    division_head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='division_head_qar_reports', help_text="Division Head")
    section_head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='section_head_qar_reports', help_text="Section Head")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_qar_reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_qar_reports')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'QAR Report'
        verbose_name_plural = 'QAR Reports'
        unique_together = ['product_batch', 'report_number']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"QAR Report - {self.report_number} - {self.product_batch.batch_id}"
    
    def get_formatted_report_number(self):
        """Get formatted report number"""
        return self.report_number
    
    def get_formatted_date(self):
        """Get formatted report date"""
        return self.report_date.strftime('%d/%m/%Y')
    
    def is_complete(self):
        """Check if the QAR report is complete"""
        required_fields = [
            'introduction', 'scope', 'batch_summary', 'end_use', 
            'processing_agency', 'raw_materials_qa', 'components_qa',
            'test_results', 'quality_assurance', 'conclusion'
        ]
        return all(getattr(self, field) for field in required_fields)
