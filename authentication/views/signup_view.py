from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.serializers.signup_serializer import UserSignupSerializer
from qdpc.core.modelviewset import BaseModelViewSet
from qdpc.core import constants
from qdpc.services.login_service import LoginService
from qdpc_core_models.models.center import Center
from qdpc_core_models.models.division import Division
from qdpc_core_models.models.user_type import UserType
from django.http import JsonResponse
from django.shortcuts import render, redirect
class Signup(BaseModelViewSet):
    permission_classes = [AllowAny]  
    authentication_classes = []     

    def get(self, request):
        context = {
            'divisions': self.get_all_obj(model_name=Division),
            'centers': self.get_all_obj(model_name=Center),
            'user_types': self.get_all_obj(model_name=UserType),
        }
        return render(request, 'regn.html',context)
    def post(self, request):
        """ Handle POST requests to register a new user """
        data = {}
        success = False
        message = constants.SIGNUP_FAILED
        status_code = status.HTTP_400_BAD_REQUEST
        
        try:
            
            # Handle user signup via the service
            data = request.data
            if data:
                success, status_code, data, message = LoginService.signup_user(data=data)
                print(f"Signup service response: success={success}, status_code={status_code}, data={data}")
            else:
                message = "No data received"
        except Exception as ex:
            # Log the exception for debugging purposes
            print(f"Error during signup: {ex}")
            success = False
            message = str(ex)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        # Render response back to the client
        return self.render_response(data, success, message, status_code)
    
    
    # def get_divisions(request, center_id):
    #     if request.method == 'GET':
    #         # Query the divisions based on the center_id
    #         divisions = Division.objects.filter(center_id=center_id).all
    #         division_list = list(divisions)  # Convert the QuerySet to a list
    #         return JsonResponse(division_list, safe=False)
        
    def get_centers(request):
        user_type_id = request.GET.get('user_type_id')
        user_type = UserType.objects.get(id=user_type_id)
        centers = Center.objects.filter(user_type=user_type)
        data = []
        for center in centers:
            data.append({
                'id': center.id,
                'name': center.name
            })
        return JsonResponse(data, safe=False)