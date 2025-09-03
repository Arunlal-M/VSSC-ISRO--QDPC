from qdpc.core import constants
from django.conf import settings
from rest_framework import status
# from qdpc_core_models.models.user import User
from component.core.helpers import ComponentManager
import traceback


class ComponentService:
    "ComponentService to make all the component operations"


    @classmethod

    def get_component_list(cls,pk=None,*args,**kwargs):
        try:
           component_manager = ComponentManager()
           success, status_code, data, message = component_manager.component_list_fetch(pk=pk, *args,**kwargs)
        except Exception as e:
            print(f"Exception in get_component_list: {e}")
            traceback.print_exc()
            message = constants.COMPONENT_FETCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Failed to fetch component list"}

        return success, status_code, data, message

    @classmethod

    def get_component_batch_list(cls,pk=None,*args,**kwargs):
        try:
            component_manager = ComponentManager()
            success, status_code, data, message = component_manager.component_batch_fetch(pk=None, *args,**kwargs)
        except Exception as e:
            print(f"Exception in get_component_batch_list: {e}")
            traceback.print_exc()
            message = constants.COMPONENT_BATCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Failed to fetch component batch list"}

        return success, status_code, data, message
    


    @classmethod

    def add_component_bach_add(cls,data):
        print(data)
        try:
            print(data,"data2")
            component_manager = ComponentManager()
            success, status_code, data, message = component_manager.component_batch_add(data=data)
        except Exception as e:
            print(f"Exception in add_component_bach_add: {e}")
            traceback.print_exc()
            message = constants.COMPONENT_BATCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Failed to add component batch"}

        return success, status_code, data, message
    
    @classmethod
    def add_component_add(cls, data):
        print(data, "Servicesss")
        try:
            component_manager =ComponentManager()
            success, status_code, data, message = component_manager.component_add(data=data)
            print(success, status_code, data, message, "What I obtained after service")
        except Exception as e:
            print("Entered except here")
            print(f"Exception: {e}")
            traceback.print_exc()  # This will print the full traceback
            message = constants.COMPONENT_BATCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Failed to add component"}

        return success, status_code, data, message

