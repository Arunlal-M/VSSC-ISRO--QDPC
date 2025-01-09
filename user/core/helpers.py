from qdpc_core_models.models.user import User
from authentication.serializers.login_serializer import LoginSerializer
from qdpc.core.user_builder import UserBuilder 
from rest_framework import status
from qdpc.core import constants
from user.serializers.userlist_serializer import UserListSerializer
from user.serializers.userupdate_serializer import UserUpdateSerializer




class UserManager:
    "Used to manage all opeations of the user module"

    def user_fetch(cls, data, *args, **kwargs):
        response_data = {}
        success = False
        status_code = status.HTTP_400_BAD_REQUEST
        message = constants.USER_FETCH_FAILED
        users = UserBuilder.get_users(data)
        if users.exists():
            serializer = UserListSerializer(users, many=True)
            response_data = serializer.data
            success = True
            message = constants.RETRIVED_USER_SUCCESS
            status_code = status.HTTP_200_OK
        else:
            message = constants.USER_NOT_FOUND_IN_GROUP

        return success, status_code, response_data, message
    
    @classmethod
    def update_user(cls,user_id, data, *args, **kwargs):
        response_data = {}
        success = False
        status_code = status.HTTP_400_BAD_REQUEST
        message = constants.USER_UPDATE_FAILED

        try:
            print(user_id,"userid i got")
            users = User.objects.filter(id=user_id)
            if users.exists():
                print("user exists")
                user = users.first()  
                print(data,"data i got")
                serializer = UserUpdateSerializer(user, data=data, partial=True)
                if serializer.is_valid():
                    print("seriliazr is valid")
                    serializer.save()
                    response_data = serializer.data
                    success = True
                    status_code = status.HTTP_200_OK
                    message = constants.USER_UPDATE_SUCCESS
                else:
                    print("serilizer not valid")
                    response_data = serializer.errors
                    message = constants.USER_UPDATE_FAILED
                    status_code = status.HTTP_400_BAD_REQUEST
          
        except Exception as e:
            # Handle any other unexpected exceptions
           
            response_data = {"error": str(e)}
            message = constants.USER_UPDATE_FAILED
            status_code = status.HTTP_400_BAD_REQUEST
          

        return success, status_code, response_data, message



