from qdpc.core import constants
from django.conf import settings
from rest_framework import status
from qdpc_core_models.models.user import User
from user.core.helpers import UserManager


class UserService:
    "UserService to make all the user operations"

    @classmethod

    def get_user_list(cls, data, *args, **kwargs):
        if data:
            user_manager = UserManager()
            success, status_code, data, message = user_manager.user_fetch(data=data, *args, **kwargs)
        else:
            message = constants.USER_FETCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Invalid data"}

        return success, status_code, data, message
    
    @classmethod
    def update_user(cls, user_id, data, *args, **kwargs):
        """ Service method to update user details """
        if data:
            print("entered data")
            user_manager = UserManager()
            success, status_code, response_data, message = user_manager.update_user(user_id=user_id, data=data, *args, **kwargs)
        else:
            message = constants.USER_FETCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            response_data = {"error": message}

        return success, status_code, response_data, message




