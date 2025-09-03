# from rest_framework import serializers
# from qdpc_core_models.models.raw_material_acceptence_test import RawMaterialAcceptanceTest
# from qdpc_core_models.models.raw_materialbach import RawMaterialBatch
# from qdpc_core_models.models.raw_material import RawMaterial
# from qdpc_core_models.models.acceptance_test import AcceptanceTest
# from qdpc_core_models.models.source import Sources
# from qdpc_core_models.models.supplier import Suppliers
# from qdpc_core_models.models.grade import Grade



# class RawMaterialAcceptanceTestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RawMaterialAcceptanceTest
#         fields = [
#             'batch_id',
#             'raw_material',
#             'acceptance_test',  # ForeignKey field that needs the primary key
#             'test_value',
#             'sources',
#             'suppliers',
#             'grade',
#             'min_value',
#             'max_value',
#             'file',
#             'status',
#             'remark',
#         ]

#     # Set related fields to PrimaryKeyRelatedField to accept IDs
#     raw_material = serializers.PrimaryKeyRelatedField(queryset=RawMaterial.objects.all())
#     acceptance_test = serializers.PrimaryKeyRelatedField(queryset=AcceptanceTest.objects.all())
#     sources = serializers.PrimaryKeyRelatedField(queryset=Sources.objects.all())
#     suppliers = serializers.PrimaryKeyRelatedField(queryset=Suppliers.objects.all())
#     grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all(), required=False, allow_null=True)  # Nullable grade

#     def create(self, validated_data):
#         return RawMaterialAcceptanceTest.objects.create(**validated_data)

#     # def get_sampling_plan_url(self, obj):
#     #     request = self.context.get('request')
#     #     if request is not None and obj.sampling_plan:
#     #         return request.build_absolute_uri(obj.sampling_plan.url)
#     #     elif obj.sampling_plan:
#     #         # Manually construct the URL if request is None
#     #         return f"/media/{obj.sampling_plan.url}"
#     #     return None



from rest_framework import serializers
from qdpc_core_models.models.raw_material_acceptence_test import RawMaterialAcceptanceTest
from qdpc_core_models.models.raw_material import RawMaterial
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.source import Sources
from qdpc_core_models.models.supplier import Suppliers
from qdpc_core_models.models.grade import Grade

class AcceptanceTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialAcceptanceTest
        fields = [
            'id',
            'test_value',
            'min_value',
            'max_value',
            'file',
            'status',
            'remark',
            'created_by'
        ]
    # Ensure the file field is optional to handle cases without file uploads
    file = serializers.FileField(required=False)


class RawMaterialAcceptanceTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialAcceptanceTest
        fields = [
            'batch_id',
            'raw_material',
            'sources',
            'suppliers',
            'grade',
            'test_value',
            'min_value',
            'max_value',
            'file',
            'status',
            'remark',
            'created_by',
            'acceptance_test'
        ]

    raw_material = serializers.PrimaryKeyRelatedField(queryset=RawMaterial.objects.all())
    sources = serializers.PrimaryKeyRelatedField(queryset=Sources.objects.all())
    suppliers = serializers.PrimaryKeyRelatedField(queryset=Suppliers.objects.all())
    grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all(), required=False, allow_null=True)
    acceptance_test = serializers.PrimaryKeyRelatedField(queryset=AcceptanceTest.objects.all())
    file = serializers.FileField(required=False, allow_null=True)

    def create(self, validated_data):
        return RawMaterialAcceptanceTest.objects.create(**validated_data)
    
    
    
    # def validate(self, data):
    #     # Ensure shelf_life_value and shelf_life_unit are None when shelf_life_type is 'not_applicable' or 'tbd'
    #     raw_material = data.get('raw_material')
    #     if raw_material in ['acceptance_test','min_value',
    #         'max_value']:
    #         data['raw_material'] = None
    #         # data['shelf_life_unit'] = None
    #     return data