from rest_framework import serializers
from qdpc_core_models.models.grade import Grade

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'
