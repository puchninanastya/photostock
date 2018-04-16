from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        if 'detail' in response.data:
            response.data['error'] = response.data['detail']
            del response.data['detail']
        else:
            error_msg = {'error' : response.data}
            response.data = error_msg

    return response