from rest_framework import serializers
from qdpc_core_models.models.qar_report import QARReport

class QARReportSerializer(serializers.ModelSerializer):
    """Serializer for QAR Report model"""
    
    class Meta:
        model = QARReport
        fields = [
            'id',
            'product_batch',
            'report_number',
            'report_date',
            'introduction',
            'scope',
            'batch_summary',
            'end_use',
            'processing_agency',
            'process_changes',
            'impact_assessment',
            'raw_materials_qa',
            'components_qa',
            'in_process_qa',
            'inspections_qa',
            'test_results',
            'quality_assurance',
            'conclusion',
            'additional_remarks',
            'engineer',
            'division_head',
            'section_head',
            'created_by',
            'created_at',
            'updated_by',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_by', 'updated_at']
    
    def create(self, validated_data):
        """Override create to set the current user as created_by"""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Override update to set the current user as updated_by"""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['updated_by'] = request.user
        return super().update(instance, validated_data)
