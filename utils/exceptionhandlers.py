from rest_framework.views import exception_handler

from rest_framework.exceptions import ValidationError, AuthenticationFailed



def custom_exception_handler(exc, context):

    handlers = {
        'ValidationError': _handle_generic_error,
        'Http404': _handle_not_found_error,
        'PermissionDenied': _handle_permission_denied_error,
        'AuthenticationFailed': _handle_authentication_failed_error,
        'NotAuthenticated': _handle_not_authenticated_error,
    }

    response = exception_handler(exc, context)

    if response is not None:

        response.data["status_code"] = response.status_code
    exception_class = exc.__class__.__name__

    if exception_class in handlers:

        return handlers[exception_class](exc, context, response)
    return response


def _handle_generic_error(exc, context, response):

    return response
    

def _handle_authentication_failed_error(exc, context, response):

    response.data = {
        "errors" : "Authentication Failed",
        "status_code" : response.status_code
    }

def _handle_not_authenticated_error(exc, context, response):

    response.data = {
        "errors" : "Not Authenticated",
        "status_code" : response.status_code
    }

def _handle_permission_denied_error(exc, context, response):

    response.data = {
        "errors" : "Permission Denied",
        "status_code" : response.status_code
    }

def _handle_not_found_error(exc, context, response):

    response.data = {
        "errors" : "Not Found",
        "status_code" : response.status_code
    }