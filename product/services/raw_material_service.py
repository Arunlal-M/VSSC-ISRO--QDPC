from qdpc.core import constants
from django.conf import settings
from rest_framework import status
from qdpc_core_models.models.user import User
from product.core.helpers import RawMatrialManager
import traceback


class RawmaterialService:
    """Service to handle all raw material operations"""

    @classmethod
    def get_rawmaterial_list(cls, pk=None, *args, **kwargs):
        try:
            raw_material_manager = RawMatrialManager()
            success, status_code, data, message = raw_material_manager.raw_material_list_fetch(pk=pk, *args, **kwargs)
        except Exception as e:
            message = constants.USER_FETCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": str(e)}

        return success, status_code, data, message

    @classmethod
    def get_rawmateril_batch_list(cls, pk=None, *args, **kwargs):
        try:
            raw_material_manager = RawMatrialManager()
            success, status_code, data, message = raw_material_manager.raw_material_batch_fetch(pk=None, *args, **kwargs)
        except Exception as e:
            message = constants.USER_FETCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": str(e)}

        return success, status_code, data, message

    @classmethod
    def add_rawmaterial_bach_add(cls, data):
        try:
            raw_material_manager = RawMatrialManager()
            success, status_code, data, message = raw_material_manager.raw_material_batch_add(data=data)
        except Exception as e:
            message = f"Error creating raw material batch: {str(e)}"
            success = False
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            data = {"error": str(e)}

        return success, status_code, data, message

    @classmethod
    def add_rawmaterial_add(cls, data):
        try:
            raw_material_manager = RawMatrialManager()
            success, status_code, data, message = raw_material_manager.raw_material_add(data=data)
        except Exception as e:
            message = constants.USER_FETCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": str(e)}

        return success, status_code, data, message

