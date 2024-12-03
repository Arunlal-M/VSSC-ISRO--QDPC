from django.db.models import Q
from qdpc_core_models.models.user import User



class UserBuilder:
    "Used for user filtering operations"
    @staticmethod
    def create_filter_query(query_params) -> Q:
        query = Q()
      
        if query_params.get('name'):
            name = query_params.get('name')
            if name:
                query &= (
                    Q(first_name__icontains=name) |
                    Q(last_name__icontains=name) |
                    Q(username__icontains=name)
                )
        
        email = query_params.get('email')
        if email:
            query &= Q(email__exact=email)

        group_name = query_params.get('group')
        if group_name:
            query &= Q(groups__name=group_name)
        return query


    @staticmethod
    def get_users(query_params):
            queryset = User.objects.all()
            query = UserBuilder.create_filter_query(query_params)
            users = queryset.filter(query)
            return users