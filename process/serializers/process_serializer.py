from rest_framework import serializers
from qdpc_core_models.models.process import Process, ProcessStep

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'

class ProcessStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStep
        fields = '__all__'
