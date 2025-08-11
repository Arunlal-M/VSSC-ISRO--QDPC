from rest_framework import status
from qdpc.core import constants
from qdpc.services.user_service import UserService
from qdpc.core.modelviewset import BaseModelViewSet
from django.shortcuts import render, redirect
from qdpc_core_models.models.user import User
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from qdpc_core_models.models.center import Center
from qdpc_core_models.models.role import Role
from qdpc_core_models.models.user_type import UserType
from qdpc_core_models.models.division import Division
from user.serializers.userupdate_serializer import UserUpdateSerializer
class UserFetch(BaseModelViewSet):
    authentication_classes = [TokenAuthentication]
    """ User List API for qdpc application"""

    def post(self, request):
        data=request.query_params
        success = False
        message = constants.USER_FETCH_FAILED
        status_code = status.HTTP_403_FORBIDDEN
        try:
            success, status_code, data, message =UserService.get_user_list(data)
        except Exception as ex:
            success = False
            message = constants.USER_FETCH_FAILED
            status_code = status.HTTP_400_BAD_REQUEST
            
        return self.render_response(data, success, message, status_code)




class UserListView(BaseModelViewSet):
    """""user list api to fetch all the user to user list"""
   
    def get(self, request, user_id=None):
        if user_id:
            user_data = self.get_user_data(user_id)
            print(user_data)

            all_divisions = self.get_all_obj(model_name=Division)
            all_roles= self.get_all_obj(model_name=Role)
            all_centres=self.get_all_obj(model_name=Center)
            all_usertypes=self.get_all_obj(model_name=UserType)
           
            # all_roles = 
            user_data['all_divisions'] = [{'id': division.id, 'name': division.name} for division in all_divisions]
            user_data['all_centres'] = [{'id': centre.id, 'name': centre.name} for centre in all_centres]
            user_data['all_roles'] = [{'id': role.id, 'name': role.name} for role in all_roles]
            user_data['all_usertypes'] = [{'id': usertype.id, 'name': usertype.name} for usertype in all_usertypes]
            return Response({'data': user_data}, status=status.HTTP_200_OK)
        
        else:
            users = User.objects.all()
            all_roles = self.get_all_obj(model_name=Role)
            context = {
            'users': users,
            'all_roles': [{'id': role.id, 'name': role.name} for role in all_roles]
             }
        
            return render(request, 'usernewone.html', context)

    def get_user_data(self, user_id):
        user = get_object_or_404(User, id=user_id)
        user_data = {
            'userid':user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.phone_number,
            'desired_salutation': user.desired_salutation,
            'centre': [centre.id for centre in user.centre.all()],
            'divisions': [division.id for division in user.divisions.all()],
            'role': [role.id for role in user.role.all()],
            'usertype': user.usertype.id if user.usertype else None,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_approved': user.is_approved,
        }
        return user_data
    

    

    def put(self, request, user_id):
        data = {}
        success = False
        message = "Invalid data"
        status_code = status.HTTP_400_BAD_REQUEST
        
        try:
            print(user_id,"user id which is passed")
            user = User.objects.get(id=user_id)
            print(user,"The user i am doing put operation")
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                print("serilaizer is valid")
                serializer.save()
                data = serializer.data
                print(data,"What i got data")
                success = True
                message = "User updated successfully"
                status_code = status.HTTP_200_OK
            else:
                data = serializer.errors
        except User.DoesNotExist:
            message = "User not found"
            status_code = status.HTTP_404_NOT_FOUND

        return self.render_response(data,success, message, status_code)


    # def update_user_role(self, request, user_id):
        
    #     try:
    #         user = User.objects.get(id=user_id)
    #         roles = request.data.get('roles', [])  # Get selected roles from request
    #         user.role.set(roles)  # Assign selected roles to the user
    #         user.save()
    #         return self.render_response({}, True, "Role updated successfully", status.HTTP_200_OK)
    #     except User.DoesNotExist:
    #         return self.render_response({}, False, "User not found", status.HTTP_404_NOT_FOUND)

class UserProfileView(BaseModelViewSet):
    def get(self,request,format=None):
        users = User.objects.all()
        all_roles= self.get_all_obj(model_name=Role)
        context = {
            "users":users,
           "all_roles": all_roles

        }
        return render(request, 'index.html', context)
