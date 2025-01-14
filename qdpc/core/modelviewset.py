
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .helpers import ResponseInfo
from qdpc_core_models.models import *


class QueryParamTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # Check for token in query params
        token = request.GET.get('token', None)
        if token:
            # Manually authenticate the token
            return self.authenticate_credentials(token)
        return None


class BaseModelViewSet(APIView,QueryParamTokenAuthentication):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super(BaseModelViewSet, self).__init__(**kwargs)
        self.response = ResponseInfo().response

    def get_object_id(self,model_name,id,*args, **kwargs):

        queryset=model_name.objects.filter(id=id)

        return queryset
    
    def get_all_obj(self,model_name,*args, **kwargs):
        queryset=model_name.objects.all()

        return queryset


    def render_response(self, data, success, message, status,
                        token="", data_to_list=True, actual_exception=None):

        if isinstance(data, dict):
            data = [data] if data else []

        response = self.response
        response['success'] = success
        if actual_exception:
            message = str(message) + " - " + str(actual_exception)
        response['message'] = message
        response['result'] = data
        response['status'] = status
        return Response(response)



class BaseViewSet(APIView):
    

    def __init__(self, **kwargs):
        super(BaseViewSet, self).__init__(**kwargs)
        self.response = ResponseInfo().response

    def get_object_id(self,model_name,id,*args, **kwargs):

        queryset=model_name.objects.filter(id=id)

        return queryset
    
    def get_all_obj(self,model_name,*args, **kwargs):
        queryset=model_name.objects.all()

        return queryset


    def render_response(self, data, success, message, status,
                        token="", data_to_list=True, actual_exception=None):

        if isinstance(data, dict):
            data = [data] if data else []

        response = self.response
        response['success'] = success
        if actual_exception:
            message = str(message) + " - " + str(actual_exception)
        response['message'] = message
        response['result'] = data
        response['status'] = status
        return Response(response)
