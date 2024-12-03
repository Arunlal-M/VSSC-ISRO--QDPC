# from qdpc.core import constants
# from django.conf import settings
# from rest_framework import status
# from qdpc_core_models.models.raw_material import RawMaterial
# from product.core.helpers import RawMatrialManager



# class RawmaterialListService:
#     "UserService to make all the user operations"

#     @classmethod

#     def get_rawmaterial_list(cls,pk=None,*args,**kwargs):
#         try:
#             raw_material_manager = RawMatrialManager()
#             is_success, status_code, data, message = raw_material_manager.raw_material_list_fetch(pk=None, *args,**kwargs)
#         except:
#             message = constants.USER_FETCH_FAILED
#             is_success = False
#             status_code = status.HTTP_400_BAD_REQUEST
#             data = {"error": "Invalid data"}

#         return is_success, status_code, data, message

#     @classmethod

#     def add_rawmaterial_bach_add(cls,data):

#         try:
#             user_manager = RawMatrialManager()
#             is_success, status_code, data, message = user_manager.raw_material_batch_add(data=data)
#         except:
#             message = constants.USER_FETCH_FAILED
#             is_success = False
#             status_code = status.HTTP_400_BAD_REQUEST
#             data = {"error": "Invalid data"}

#         return is_success, status_code, data, message
