# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework import status
# from rest_framework.response import Response
# from qdpc_core_models.models.raw_material import RawMaterial
# from qdpc_core_models.models.unit import Unit
# from product.serializers.raw_material_acceptance_test_seraizler import RawMaterialAcceptanceTestSerializer
# from qdpc.core.modelviewset import BaseModelViewSet
# from django.shortcuts import render, redirect

# class RawMaterialAcceptanceTestAdd(BaseModelViewSet):
#     parser_classes = [MultiPartParser, FormParser]

#     """ Raw Material Acceptance Test API for qdpc application"""

#     def get(self, request):
#         raw_materials = self.get_all_obj(model_name=RawMaterial)
#         units = self.get_all_obj(model_name=Unit)
#         context = {
#             'raw_materials': raw_materials,
#             'units': units
#         }
#         return render(request, 'rmacceptance-test.html', context)

#     def post(self, request):
#         # Validate the incoming data using the serializer
#         serializer = RawMaterialAcceptanceTestSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             success = True
#             message = 'Raw Material Acceptance Test added successfully!'
#             data = serializer.data
#             status_code = status.HTTP_201_CREATED
#         else:
#             print("Validation errors:", serializer.errors)
#             success = False
#             message = 'Validation failed.'
#             status_code = status.HTTP_400_BAD_REQUEST
#             data = serializer.errors

#         return self.render_response(data, success, message, status_code)
