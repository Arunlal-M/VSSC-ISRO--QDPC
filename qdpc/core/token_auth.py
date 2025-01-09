from rest_framework.authentication import TokenAuthentication
from .helpers import ResponseInfo
from rest_framework import HTTP_HEADER_ENCODING
from .exception import*
from django.utils import timezone
from datetime import timedelta

class TokenInQueryAuthentication(TokenAuthentication):
    """
    Extending token authentication,
    now you can pass tokens as GET parameter
    """
    msg = ResponseInfo().response
    expire_token = False

    def authenticate(self, request):
        auth = self.get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            self.msg["message"] = (
                'Invalid token header. No credentials provided.')
            raise AuthenticationError(self.msg)
        elif len(auth) > 2:
            self.msg["message"] = (
                'Invalid token header. Token string should not contain spaces.')
            raise AuthenticationError(self.msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            self.msg["message"] = ('Invalid token header.'
                                    ' Token string should not contain invalid characters.')
            raise AuthenticationError(self.msg)

        return self.authenticate_credentials(token)

    @classmethod
    def get_authorization_header(cls, request):
        """
        Return request's 'Authorization:' header, as a bytestring.
        Hide some test client ickyness where the header can be unicode.
        """
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if not auth:
            auth = request.GET.get('token', "")
            if auth:
                auth = 'Token ' + auth
        if isinstance(auth, type('')):
            # Work around Django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            self.msg["message"] = ('Invalid token.')
            raise AuthenticationError(self.msg)

        if not token.user.is_active:
            self.msg["message"] = ('User inactive or deleted.')
            token.delete()
            raise AuthenticationError(self.msg)

        # if self.expire_token:

        #     if timezone.now() > token.created + timedelta(
        #             seconds=settings.TOKEN_EXPIRY):
        #         self.msg["message"] = ("Token expired, please login again")
        #         token.delete()
        #         raise AuthenticationError(self.msg)
        #     if timezone.now() > token.created + timedelta(minutes=2):
        #         token.created = timezone.now()
        #         token.save()
        else:
            token.created = timezone.now()
            token.save()

        return (token.user, token)
