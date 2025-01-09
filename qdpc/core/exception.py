from rest_framework.exceptions import APIException, _get_error_details
from rest_framework import status
from django.utils import six


class CommonException(APIException):
    """
    A common API exception class,
    every API exceptions should be derived from here.
    """
    default_detail = _('API Exception')
    default_code = 'exception'

    def __init__(self, detail, status_code=None, code=None):
        if status_code:
            self.status_code = status_code
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect may errors together, so the
        # details should always be coerced to a list if not already.
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)

    def __str__(self):
        return six.text_type(self.detail)


class AuthenticationError(CommonException):
    """
    Authentication Error
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Authentication failed')
    default_code = 'unauthenticated'


class PermissionDenied(CommonException):
    """
    403
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('Permission Denied')
    default_code = 'forbidden'


class LoginError(CommonException):
    """
    Authentication Error
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Authentication failed')
    default_code = 'unauthenticated'
